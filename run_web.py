import os
import sys

import uvicorn


async def _run_server():
    # Get Config Path
    config_dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web/config'))

    # Add To PATH Config Dir
    sys.path.append(config_dir_path)

    # Run FastAPI Application
    uvicorn_cmd = "app:app"
    uvicorn.run(uvicorn_cmd, host="0.0.0.0", port=8080, reload=True)


if __name__ == "__main__":
    import asyncio

    # Run Async Module
    asyncio.run(_run_server())
