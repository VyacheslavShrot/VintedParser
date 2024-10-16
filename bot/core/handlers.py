import asyncio

from aiogram.types import Message, InputMediaPhoto
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests

from bot.config.logger import logger


class Handlers:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Handlers, cls).__new__(cls)
            return cls._instance
        if cls._instance:
            raise Exception("Only one instance of Handlers can be created.")

    async def handle_text_input(
            self,
            message: Message
    ) -> None:
        """
        Any Text Message
        :param message: Default Aiogram Telegram Message
        :type message: Message
        """
        browser = None

        logger.info("\n----Text Input Handler is Starting")
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            browser = webdriver.Chrome(options=options)
            logger.info("success connect to local browser")

            # start_url = 'https://www.vinted.pl/catalog?search_text=&brand_ids[]=73306&search_id=17785961064&order=newest_first&time=1729020473'

            start_url = message.text
            logger.info(f"{start_url}")

            browser.get(start_url)

            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
            )

            button_cookie = browser.find_element(By.ID, 'onetrust-accept-btn-handler')
            if button_cookie.is_displayed() and button_cookie.is_enabled():
                button_cookie.click()

            existed_boxes: list = []

            while True:
                WebDriverWait(browser, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'new-item-box__container'))
                )

                item_boxes = browser.find_elements(By.CLASS_NAME, 'new-item-box__container')

                try:
                    for box in item_boxes[:5]:
                        unique_id = box.get_attribute('data-testid')

                        if unique_id not in existed_boxes:
                            existed_boxes.append(unique_id)

                            link = box.find_element(By.CSS_SELECTOR, '.new-item-box__overlay.new-item-box__overlay--clickable')
                            href = link.get_attribute('href')

                            images = box.find_elements(By.CLASS_NAME, 'web_ui__Image__content')
                            src_list = [img.get_attribute('src') for img in images if img.get_attribute('src')]

                            price = box.find_element(
                                By.CSS_SELECTOR, '.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left.web_ui__Text__muted'
                            )

                            if href and images and price.text:
                                response = f"{href}\n{price.text}"

                                if len(src_list) == 1:
                                    await message.answer_photo(src_list[0], caption=response)
                                elif len(src_list) > 1:
                                    media = [InputMediaPhoto(media=src) for src in src_list]
                                    media[0].caption = response
                                    await message.answer_media_group(media)

                                await asyncio.sleep(1)
                except Exception as e:
                    logger.error(f"Error occurred while iterate in boxes | {e}")
                    continue

                browser.refresh()
        except Exception as e:
            logger.error(
                f"An unexpected error in Text Input Handler | {e}"
            )
            browser.close()
