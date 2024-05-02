import json
import time
import cv2

from av import VideoFrame
from fastapi import FastAPI, WebSocket
from SparkleLogging.utils.core import LogManager
from fastapi.responses import HTMLResponse

from aiortc import (
    MediaStreamTrack,
    RTCDataChannel,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
)

app = FastAPI()
logger = LogManager().GetLogger('main')  # 初始化日志器

pcs = set()  # RTCPeerConnection集合


@app.get("/", response_class=HTMLResponse)
async def root():
    html = open("static/index.html", "r", encoding="utf-8").read()
    return html


@app.websocket("/offer")
async def offer(websocket: WebSocket):
    await websocket.accept()
    params = await websocket.receive_json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    await server(pc, offer)
    await websocket.send_json(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        )


async def server(pc, offer):
    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        logger.info("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        logger.info("======= received track: %s" % track)
        if track.kind == "video":
            t = FrameHandler(track)
            pc.addTrack(t)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)


class FrameHandler(VideoStreamTrack):
    kind = "video"

    def __init__(self, track):
        super().__init__()
        self.track = track
        self.face_detector = cv2.CascadeClassifier("static/haarcascade_frontalface_alt.xml")
        self.face = cv2.imread("static/wu.png")

    async def recv(self):
        timestamp, video_timestamp_base = await self.next_timestamp()
        frame = await self.track.recv()
        frame = frame.to_ndarray(format="bgr24")
        s = time.time()
        face_zones = self.face_detector.detectMultiScale(
            cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)
        )
        for x, y, w, h in face_zones:
            face = cv2.resize(self.face, dsize=(w, h))
            frame[y : y + h, x : x + w] = face
        frame = VideoFrame.from_ndarray(frame, format="bgr24")
        frame.pts = timestamp
        frame.time_base = video_timestamp_base
        return frame


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
