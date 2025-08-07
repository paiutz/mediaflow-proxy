import os
import sys
from dotenv import load_dotenv

# ✅ Load .env from the directory of the .exe or .py file
base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
dotenv_path = os.path.join(base_path, ".env")
load_dotenv(dotenv_path)

# ✅ Set fallback for missing env vars
os.environ.setdefault("API_PASSWORD", "changeme")

# ✅ Optional: Debug log API_PASSWORD only when DEBUG=true
if os.getenv("DEBUG", "false").lower() == "true":
    print(f"🔐 API_PASSWORD: {os.getenv('API_PASSWORD')}")

# ✅ Import the actual FastAPI app
from mediaflow_proxy.main import app

def run():
    import uvicorn

    is_frozen = getattr(sys, 'frozen', False)

    # ✅ Check for HTTPS cert files in the same folder
    cert_file = os.path.join(base_path, "cert.pem")
    key_file = os.path.join(base_path, "key.pem")
    ssl_args = {}

    if os.path.exists(cert_file) and os.path.exists(key_file):
        ssl_args["ssl_certfile"] = cert_file
        ssl_args["ssl_keyfile"] = key_file
        print("🔐 HTTPS enabled with cert.pem and key.pem")
    else:
        print("⚠️ No cert.pem/key.pem found. Running over HTTP.")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8888,
        log_level="info",
        workers=1,
        reload=not is_frozen,
        **ssl_args
    )

if __name__ == "__main__":
    run()
