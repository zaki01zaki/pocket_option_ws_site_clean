from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Trading WebSocket API</title>
        </head>
        <body>
            <h1>Welcome to the Trading WebSocket API</h1>
            <p>The server is running successfully.</p>
        </body>
    </html>
    """

# إذا كنت تريد اختبار المشروع محليًا يمكنك إضافة:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
