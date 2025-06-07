import threading
import time
import requests
from fastapi import FastAPI
import uvicorn

API_TOKEN = "your_cloudflare_api_token"
ZONE_ID = "your_cloudflare_zone_id"
RECORD_ID = "your_dns_record_id"

VPS_LIST = [
    {"name": "vps1", "ip": "192.0.2.1", "health_url": "http://192.0.2.1"},
    {"name": "vps2", "ip": "198.51.100.1", "health_url": "http://198.51.100.1"},
]

def check_health(url):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200 and r.json().get("status") == "ok":
            return True
    except:
        return False
    return False

def get_current_dns_ip():
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200 and res.json().get("success"):
        return res.json()["result"]["content"]
    return None

def update_dns(ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "type": "A",
        "name": "vps.iws.lol",
        "content": ip,
        "ttl": 60,
        "proxied": False
    }
    res = requests.put(url, json=data, headers=headers)
    return res.json()

def main():
    current_ip = get_current_dns_ip()
    if not current_ip:
        print("⚠️ Could not fetch current DNS IP from Cloudflare.")
        return

    for vps in VPS_LIST:
        if check_health(vps["health_url"]):
            if current_ip == vps["ip"]:
                print(f"✅ {vps['name']} is healthy and DNS is already set. No update needed.")
            else:
                print(f"🔁 {vps['name']} is healthy but DNS IP is different. Updating...")
                result = update_dns(vps["ip"])
                if result.get("success"):
                    print("✅ DNS updated successfully.")
                else:
                    print("❌ Failed to update DNS:", result)
            return

    print("🚫 No healthy VPS found. DNS not updated.")

def background_loop():
    while True:
        main()
        time.sleep(60)

app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    threading.Thread(target=background_loop, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=80)
