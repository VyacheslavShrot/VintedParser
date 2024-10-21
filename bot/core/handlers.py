import asyncio

from aiogram.types import Message, InputMediaPhoto
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bot.config.logger import logger


class Handlers:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Handlers, cls).__new__(cls)
            return cls._instance
        if cls._instance:
            raise Exception("Only one instance of Handlers can be created.")

    def __init__(self):
        super().__init__()
        self.task = None

        self.task_2 = None

    async def handle_text_input(
            self,
            message: Message
    ) -> None:
        """
        Any Text Message
        :param message: Default Aiogram Telegram Message
        :type message: Message
        """
        logger.info("\n----Text Input Handler is Starting")
        print(len(message.text.split(" ")))
        try:
            if (self.task or self.task_2) and message.text == "стоп":
                if self.task:
                    self.task.cancel()

                if self.task_2:
                    self.task_2.cancel()

                await message.answer("Остановка обработки.")

                try:
                    await self.task
                except asyncio.CancelledError:
                    logger.info("Parsing task was cancelled.")

                self.task = None

            elif (not self.task or not self.task_2) and message.text != "стоп":
                if message.text.startswith("https://www.vinted.pl"):
                    if not self.task:
                        if len(message.text.split(" ")) == 1:
                            self.task = asyncio.create_task(self.run_parsing(message))
                        elif len(message.text.split(" ")) == 2:
                            self.task = asyncio.create_task(self.run_parsing(message, True))

                    elif not self.task_2:
                        if len(message.text.split(" ")) == 1:
                            self.task_2 = asyncio.create_task(self.run_parsing(message))
                        elif len(message.text.split(" ")) == 2:
                            self.task_2 = asyncio.create_task(self.run_parsing(message, True))

        except Exception as e:
            logger.error(
                f"An unexpected error in Text Input Handler | {e}"
            )

    async def run_parsing(
            self,
            message,
            links: bool = None
    ):
        browser = None

        logger.info("\n----Task is Starting")
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            browser = webdriver.Chrome(options=options)
            logger.info("success connect to local browser")

            if not links:
                start_url = message.text

                browser.get(start_url)

            # WebDriverWait(browser, 25).until(
            #     EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
            # )
            #
            # logger.info("Before Click Cookie Button")
            # button_cookie = browser.find_element(By.ID, 'onetrust-accept-btn-handler')
            # if button_cookie.is_displayed() and button_cookie.is_enabled():
            #     button_cookie.click()

            existed_boxes: list = []

            while True:
                if links:
                    for query in message.text.split(" "):
                        query: str  # Link of Vinted URL with Specific Category
                        if not query.startswith("https://www.vinted.pl"):
                            continue

                        browser.get(query)

                        WebDriverWait(browser, 10).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, 'new-item-box__container'))
                        )

                        item_boxes = browser.find_elements(By.CLASS_NAME, 'new-item-box__container')

                        try:
                            for box in item_boxes[:7]:
                                unique_id = box.get_attribute('data-testid')

                                if unique_id not in existed_boxes:
                                    existed_boxes.append(unique_id)

                                    """
                                    Get URL of Item
                                    """
                                    link = box.find_element(By.CSS_SELECTOR, '.new-item-box__overlay.new-item-box__overlay--clickable')
                                    href = link.get_attribute('href')

                                    """
                                    Get Size of Item
                                    """
                                    size_boxes = box.find_elements(By.CLASS_NAME, 'new-item-box__description')
                                    size_element = size_boxes[1].find_element(By.CSS_SELECTOR,
                                                                              '.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left')
                                    size = size_element.text

                                    """
                                    Get Images of Item
                                    """
                                    images = box.find_elements(By.CLASS_NAME, 'web_ui__Image__content')
                                    src_list = [img.get_attribute('src') for img in images if img.get_attribute('src')]
                                    src_list.pop(0)

                                    """
                                    Get Price of Item
                                    """
                                    price = box.find_element(
                                        By.CSS_SELECTOR, '.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left.web_ui__Text__muted'
                                    )

                                    if href and images and price.text and size:
                                        response = f"{price.text}\n{size}\n\n{href}"

                                        if len(src_list) == 1:
                                            await message.answer_photo(src_list[0], caption=response)
                                        elif len(src_list) > 1:
                                            media = [InputMediaPhoto(media=src) for src in src_list]
                                            media[0].caption = response
                                            await message.answer_media_group(media)

                                        await asyncio.sleep(2)
                        except Exception as e:
                            logger.error(f"Error occurred while iterate in boxes | {e}")
                            continue
                else:
                    WebDriverWait(browser, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'new-item-box__container'))
                    )

                    item_boxes = browser.find_elements(By.CLASS_NAME, 'new-item-box__container')

                    try:
                        for box in item_boxes[:7]:
                            unique_id = box.get_attribute('data-testid')

                            if unique_id not in existed_boxes:
                                existed_boxes.append(unique_id)

                                """
                                Get URL of Item
                                """
                                link = box.find_element(By.CSS_SELECTOR, '.new-item-box__overlay.new-item-box__overlay--clickable')
                                href = link.get_attribute('href')

                                """
                                Get Size of Item
                                """
                                size_boxes = box.find_elements(By.CLASS_NAME, 'new-item-box__description')
                                size_element = size_boxes[1].find_element(By.CSS_SELECTOR, '.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left')
                                size = size_element.text

                                """
                                Get Images of Item
                                """
                                images = box.find_elements(By.CLASS_NAME, 'web_ui__Image__content')
                                src_list = [img.get_attribute('src') for img in images if img.get_attribute('src')]
                                src_list.pop(0)

                                """
                                Get Price of Item
                                """
                                price = box.find_element(
                                    By.CSS_SELECTOR, '.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left.web_ui__Text__muted'
                                )

                                if href and images and price.text and size:
                                    response = f"{price.text}\n{size}\n\n{href}"

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

                    await asyncio.sleep(3)

                    browser.refresh()

        except Exception as e:
            logger.error(
                f"An unexpected error in Task | {e}"
            )
            browser.close()

            self.task = asyncio.create_task(self.run_parsing(message))


