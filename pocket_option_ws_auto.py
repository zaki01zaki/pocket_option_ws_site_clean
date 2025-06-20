
# نسخة محسنة مع دعم API و WebSocket Forwarding

import asyncio
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import websockets
from fastapi import FastAPI, WebSocket
import uvicorn

# ========== استخراج رابط WebSocket بشكل دوري ==========

class PocketOptionWebSocketAutoExtractor:
    def __init__(self, site_url="https://pocketoption.com", extraction_interval=300):
        self.site_url = site_url
        self.extraction_interval = extraction_interval
        self.current_ws_url = None

    def extract_websocket_url(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")

        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        driver = webdriver.Chrome(service=Service(), options=options, desired_capabilities=caps)
        driver.get(self.site_url)

        print("✅ جاري استخراج رابط WebSocket... الرجاء الانتظار...")
        time.sleep(30)

        logs = driver.get_log('performance')
        ws_urls = []

        for entry in logs:
            message = entry['message']
            if 'Network.webSocketCreated' in message:
                if 'wss://' in message:
                    start = message.find('wss://')
                    end = message.find('"', start)
                    url = message[start:end]
                    if url not in ws_urls:
                        ws_urls.append(url)

        driver.quit()

        if ws_urls:
            print("✅ تم العثور على رابط WebSocket:", ws_urls[0])
            return ws_urls[0]
        else:
            print("❌ لم يتم العثور على رابط WebSocket. سيتم إعادة المحاولة لاحقًا.")
            return None

    async def update_websocket_url_periodically(self):
        while True:
            new_url = self.extract_websocket_url()
            if new_url:
                self.current_ws_url = new_url
            await asyncio.sleep(self.extraction_interval)


# ========== عميل WebSocket متكامل ==========

class RealTimeWebSocketClient:
    def __init__(self, url_getter, on_price_update):
        self.url_getter = url_getter
        self.on_price_update = on_price_update

    async def connect(self):
        while True:
            if self.url_getter.current_ws_url:
                try:
                    async with websockets.connect(self.url_getter.current_ws_url) as websocket:
                        print("✅ متصل مع WebSocket: ", self.url_getter.current_ws_url)
                        while True:
                            message = await websocket.recv()
                            data = json.loads(message)

                            if 'price' in data and 'asset' in data:
                                await self.on_price_update(data['asset'], data['price'])
                except Exception as e:
                    print(f"❌ حدث خطأ: {e}, سيتم إعادة المحاولة خلال 5 ثواني...")
                    await asyncio.sleep(5)
            else:
                print("🔄 في انتظار رابط WebSocket...")
                await asyncio.sleep(5)


# ========== تخزين الأسعار ==========

class PriceStore:
    def __init__(self):
        self.prices = {}
        self.subscribers = set()

    async def update_price(self, asset, price):
        self.prices[asset] = price
        print(f"🔔 {asset}: {price}")

        message = json.dumps({"asset": asset, "price": price})
        await self.broadcast(message)

    async def broadcast(self, message):
        for ws in self.subscribers:
            try:
                await ws.send_text(message)
            except Exception:
                pass


# ========== إعداد API ==========

app = FastAPI()
store = PriceStore()

@app.get("/latest-prices")
async def get_latest_prices():
    return store.prices

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    store.subscribers.add(websocket)
    print("✅ عميل WebSocket متصل")

    try:
        while True:
            await websocket.receive_text()
    except Exception:
        pass
    finally:
        store.subscribers.remove(websocket)
        print("❌ عميل WebSocket تم فصله")


# ========== التشغيل المتكامل ==========

async def main():
    extractor = PocketOptionWebSocketAutoExtractor()

    asyncio.create_task(extractor.update_websocket_url_periodically())
    client = RealTimeWebSocketClient(extractor, store.update_price)
    asyncio.create_task(client.connect())

    config = uvicorn.Config(app, host="0.0.0.0", port=10000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
