import os
import sys
from dotenv import load_dotenv

# Determine base path whether running as EXE or .py
base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)

# Load .env next to EXE or script
dotenv_path = os.path.join(base_path, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print("⚠️ No .env file found")

# Set fallback values
os.environ.setdefault("API_PASSWORD", "changeme")

if os.getenv("DEBUG", "false").lower() == "true":
    print(f"🔐 API_PASSWORD: {os.getenv('API_PASSWORD')}")

port = int(os.getenv("PORT", 8888))  # Default to 8888 if PORT not set

# Import FastAPI app AFTER env setup
from mediaflow_proxy.main import app

def run():
    import uvicorn

    is_frozen = getattr(sys, 'frozen', False)

    ssl_args = {}
    cert_key_pairs = [
        ("cert.pem", "key.pem"),
        ("fullchain.pem", "privkey.pem"),
    ]

    for cert_name, key_name in cert_key_pairs:
        cert_file = os.path.join(base_path, cert_name)
        key_file = os.path.join(base_path, key_name)
        if os.path.exists(cert_file) and os.path.exists(key_file):
            ssl_args["ssl_certfile"] = cert_file
            ssl_args["ssl_keyfile"] = key_file
            print(f"🔐 HTTPS enabled ({cert_name} + {key_name})")
            break
    else:
        print("⚠️ HTTPS certs not found, running on plain HTTP")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=not is_frozen,
        workers=1,
        log_level="info",
        **ssl_args
    )

if __name__ == "__main__":
    run()
