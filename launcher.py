# launcher.py
import os
import sys
from dotenv import load_dotenv

# ✅ Load .env from the directory of the .exe or .py file
base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
dotenv_path = os.path.join(base_path, ".env")
load_dotenv(dotenv_path)

# ✅ Set fallback for missing env vars
os.environ.setdefault("API_PASSWORD", "changeme")

# ✅ Import the FastAPI app
from mediaflow_proxy.main import app

def run():
    import uvicorn

    is_frozen = getattr(sys, 'frozen', False)

    ssl_certfile = os.path.join(base_path, "cert.pem")
    ssl_keyfile = os.path.join(base_path, "key.pem")

    ssl_enabled = os.path.exists(ssl_certfile) and os.path.exists(ssl_keyfile)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8888,
        log_level="info",
        workers=1,
        reload=not is_frozen,
        ssl_certfile=ssl_certfile if ssl_enabled else None,
        ssl_keyfile=ssl_keyfile if ssl_enabled else None,
    )

if __name__ == "__main__":
    run()
