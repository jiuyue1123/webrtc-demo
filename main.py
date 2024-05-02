from fastapi import FastAPI, WebSocket
from SparkleLogging.utils.core import LogManager
from fastapi.responses import HTMLResponse

app = FastAPI()
logger = LogManager().GetLogger('main')  # 初始化日志器


@app.get("/", response_class=HTMLResponse)
async def root():
    html = open("static/index.html", "r", encoding="utf-8").read()
    return html


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.websocket("/ws")
async def handler_websocket(websocket: WebSocket):
    logger.info("websocket connected")
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
