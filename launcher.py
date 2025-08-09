import os
import sys
import multiprocessing
from pathlib import Path
from dotenv import load_dotenv

# Determine base path for both development and frozen executable
if getattr(sys, 'frozen', False):
    # Running as PyInstaller executable
    base_path = Path(sys.executable).parent
else:
    # Running as Python script
    base_path = Path(__file__).parent

# Load .env file from the base path
dotenv_path = base_path / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
    print(f"✅ Loaded configuration from: {dotenv_path}")
else:
    print(f"⚠️ No .env file found at: {dotenv_path}")

# Set default environment variables
defaults = {
    "API_PASSWORD": "changeme",
    "PORT": "8888",
    "DEBUG": "false",
    "ENABLE_STREAMING_PROGRESS": "false",
    "DISABLE_HOME_PAGE": "false",
    "DISABLE_DOCS": "false",
    "DISABLE_SPEEDTEST": "false"
}

for key, default_value in defaults.items():
    os.environ.setdefault(key, default_value)

# Validate and convert port
try:
    port = int(os.getenv("PORT", 8888))
    if not (1 <= port <= 65535):
        raise ValueError(f"Port {port} is out of valid range (1-65535)")
except ValueError as e:
    print(f"❌ Invalid PORT value: {e}")
    port = 8888
    print(f"🔄 Using default port: {port}")

# Security warning for default password
if os.getenv("API_PASSWORD") == "changeme":
    print("⚠️ WARNING: You are using the default API password!")
    print("   Please change 'API_PASSWORD' in the .env file for security.")

# Debug mode info
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
if debug_mode:
    print(f"🐛 Debug mode enabled")
    print(f"🔐 API_PASSWORD: {os.getenv('API_PASSWORD')}")
    print(f"🌐 PORT: {port}")
    print(f"📁 Base path: {base_path}")

def run():
    """Run the MediaFlow Proxy server using uvicorn."""
    try:
        import uvicorn
        
        # Try to use uvloop for better performance (optional)
        try:
            import uvloop
            uvloop.install()
            print("🚀 uvloop activated for better performance")
        except ImportError:
            print("⚠️ uvloop not available, using default event loop")
        
        # Import check - make sure the module is available
        try:
            from mediaflow_proxy.main import app
        except ImportError as e:
            print(f"❌ Failed to import MediaFlow Proxy app: {e}")
            print("   Make sure mediaflow-proxy is properly installed")
            sys.exit(1)
        
        # Determine if running as frozen executable
        is_frozen = getattr(sys, 'frozen', False)
        
        # SSL certificate detection
        ssl_args = {}
        cert_combinations = [
            ("cert.pem", "key.pem"),
            ("fullchain.pem", "privkey.pem")
        ]
        
        for cert_name, key_name in cert_combinations:
            cert_file = base_path / cert_name
            key_file = base_path / key_name
            if cert_file.exists() and key_file.exists():
                ssl_args["ssl_certfile"] = str(cert_file)
                ssl_args["ssl_keyfile"] = str(key_file)
                protocol = "HTTPS"
                print(f"🔐 SSL enabled with {cert_name} + {key_name}")
                break
        else:
            protocol = "HTTP"
            print("⚠️ No SSL certificates found, using HTTP")
        
        # Worker and reload configuration
        if is_frozen:
            # For frozen executable, use multiple workers but no reload
            num_workers = max(1, min(multiprocessing.cpu_count(), 4))
            reload_mode = False
            # Use import string for multiple workers
            app_target = "mediaflow_proxy.main:app"
        else:
            # For development, use single worker with optional reload
            num_workers = 1
            reload_mode = debug_mode
            # Can use app object for single worker
            app_target = app
        
        print(f"⚙️ Starting server with {num_workers} worker(s)")
        print(f"🌐 Server will be available at: {protocol.lower()}://localhost:{port}")
        print(f"📚 API Documentation: {protocol.lower()}://localhost:{port}/docs")
        print(f"🏠 Home Page: {protocol.lower()}://localhost:{port}")
        
        if os.getenv("DISABLE_SPEEDTEST", "false").lower() != "true":
            print(f"⚡ Speed Test: {protocol.lower()}://localhost:{port}/speedtest.html")
        
        print(f"🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run the server with appropriate configuration
        if is_frozen and num_workers > 1:
            # Multiple workers - must use import string
            uvicorn.run(
                app_target,  # This will be the import string
                host="0.0.0.0",
                port=port,
                workers=num_workers,
                log_level="info" if not debug_mode else "debug",
                access_log=debug_mode,
                **ssl_args
            )
        else:
            # Single worker - can use app object or import string
            uvicorn.run(
                app_target,
                host="0.0.0.0",
                port=port,
                reload=reload_mode,
                log_level="info" if not debug_mode else "debug",
                access_log=debug_mode,
                **ssl_args
            )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        if debug_mode:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def main():
    """Main entry point."""
    print("=" * 50)
    print("🎬 MediaFlow Proxy Server")
    print("=" * 50)
    
    # Show basic info
    print(f"📁 Working directory: {base_path}")
    
    # Check if this is a frozen executable
    if getattr(sys, 'frozen', False):
        print("📦 Running as standalone executable")
    else:
        print("🐍 Running as Python script")
    
    # Check for important files
    required_files = [".env"]
    for filename in required_files:
        file_path = base_path / filename
        if file_path.exists():
            print(f"✅ Found: {filename}")
        else:
            print(f"⚠️ Missing: {filename}")
    
    print("-" * 50)
    
    # Run the server
    run()

if __name__ == "__main__":
    main()
