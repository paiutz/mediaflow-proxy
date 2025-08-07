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

# ✅ Import the actual FastAPI app
from mediaflow_proxy.main import app

def run():
    import uvicorn

    is_frozen = getattr(sys, 'frozen', False)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8888,
        log_level="info",
        workers=1,
        reload=not is_frozen
    )

if __name__ == "__main__":
    run()
