# Auto DNS Failover for VPS (with Cloudflare & FastAPI)

This script automatically monitors multiple VPS servers and dynamically updates a Cloudflare DNS A record based on the health of the VPS instances.

✅ Features:
- Health check for multiple VPS instances.
- Automatic DNS record update via Cloudflare API.
- Failover DNS switch when the active VPS becomes unavailable.
- Simple FastAPI server with a `/` health check endpoint.
- Background monitoring every 60 seconds.

🛠️ Technologies Used:
- Python
- FastAPI
- Cloudflare API
- Requests
- Uvicorn
- Threading

🔧 Configuration:
Update the following variables:
```python
API_TOKEN = "your_cloudflare_api_token"
ZONE_ID = "your_cloudflare_zone_id"
RECORD_ID = "your_dns_record_id"
