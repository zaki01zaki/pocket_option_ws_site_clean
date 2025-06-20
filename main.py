from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

# صفحة ترحيبية عند زيارة /
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Trading WebSocket API</title>
        </head>
        <body>
            <h1>🎉 Welcome to the Trading WebSocket API 🎉</h1>
            <p>The server is live and ready to accept WebSocket connections.</p>
        </body>
    </html>
    """

# WebSocket endpoint (إذا كنت تستخدم WebSocket في مشروعك)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")

# تشغيل محلي
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
