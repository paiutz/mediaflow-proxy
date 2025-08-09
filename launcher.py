import os
import sys
import multiprocessing
from dotenv import load_dotenv

# Base path (EXE o .py)
base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)

# Carica .env accanto all'EXE
dotenv_path = os.path.join(base_path, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print("⚠️ Nessun file .env trovato accanto all'app")

# Valori di default
os.environ.setdefault("API_PASSWORD", "changeme")
os.environ.setdefault("PORT", "8888")
os.environ.setdefault("DEBUG", "false")

if os.getenv("DEBUG", "false").lower() == "true":
    print(f"🔐 API_PASSWORD: {os.getenv('API_PASSWORD')}")

port = int(os.getenv("PORT", 8888))

# Importa FastAPI app
from mediaflow_proxy.main import app

def run():
    import uvicorn

    # Prova ad attivare uvloop su Windows
    try:
        import uvloop
        uvloop.install()
        print("🚀 uvloop attivato")
    except ImportError:
        print("⚠️ uvloop non disponibile (usa loop predefinito)")

    is_frozen = getattr(sys, 'frozen', False)

    ssl_args = {}
    for cert_name, key_name in [("cert.pem", "key.pem"), ("fullchain.pem", "privkey.pem")]:
        cert_file = os.path.join(base_path, cert_name)
        key_file = os.path.join(base_path, key_name)
        if os.path.exists(cert_file) and os.path.exists(key_file):
            ssl_args["ssl_certfile"] = cert_file
            ssl_args["ssl_keyfile"] = key_file
            print(f"🔐 HTTPS attivo ({cert_name} + {key_name})")
            break
    else:
        print("⚠️ Nessun certificato SSL trovato, uso HTTP")

    # Leggi WORKERS da env, fallback al numero di core CPU
    try:
        workers = int(os.getenv("WORKERS", 0))
        if workers < 1:
            raise ValueError
    except Exception:
        workers = multiprocessing.cpu_count()

    print(f"⚙️ Avvio con {workers} worker (configurati in WORKERS o default CPU)")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=not is_frozen,
        workers=workers,
        log_level="info",
        **ssl_args
    )

if __name__ == "__main__":
    run()
