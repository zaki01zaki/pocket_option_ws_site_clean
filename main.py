
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

# صفحة ترحيبية عند زيارة الرابط الرئيسي
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Pocket Option WebSocket Site</title>
        </head>
        <body>
            <h1>✅ Pocket Option WebSocket Site is Live ✅</h1>
            <p>You can now connect to the WebSocket at <code>/ws</code>.</p>
        </body>
    </html>
    """

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")

# لتشغيله محليا إذا أردت
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
