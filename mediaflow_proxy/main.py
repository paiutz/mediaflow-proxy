import asyncio
import logging
from importlib import resources

from fastapi import FastAPI, Depends, Security, HTTPException
from fastapi.security import APIKeyQuery, APIKeyHeader
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from mediaflow_proxy.configs import settings
from mediaflow_proxy.middleware import UIAccessControlMiddleware
from mediaflow_proxy.routes import proxy_router, extractor_router, speedtest_router, playlist_builder_router
from mediaflow_proxy.schemas import GenerateUrlRequest, GenerateMultiUrlRequest, MultiUrlRequestItem
from mediaflow_proxy.utils.crypto_utils import EncryptionHandler, EncryptionMiddleware
from mediaflow_proxy.utils.http_utils import encode_mediaflow_proxy_url
from mediaflow_proxy.utils.base64_utils import encode_url_to_base64, decode_base64_url, is_base64_url

# Logging setup
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# FastAPI app
app = FastAPI()

# Security
api_password_query = APIKeyQuery(name="api_password", auto_error=False)
api_password_header = APIKeyHeader(name="api_password", auto_error=False)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(EncryptionMiddleware)
app.add_middleware(UIAccessControlMiddleware)

# API key verification
async def verify_api_key(api_key: str = Security(api_password_query), api_key_alt: str = Security(api_password_header)):
    if not settings.api_password:
        return
    if api_key == settings.api_password or api_key_alt == settings.api_password:
        return
    raise HTTPException(status_code=403, detail="Could not validate credentials")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/favicon.ico")
async def get_favicon():
    return RedirectResponse(url="/logo.png")

@app.get("/speedtest")
async def show_speedtest_page():
    return RedirectResponse(url="/speedtest.html")

@app.post("/generate_encrypted_or_encoded_url", deprecated=True, tags=["url"])
async def generate_encrypted_or_encoded_url(request: GenerateUrlRequest):
    return {"encoded_url": (await generate_url(request))["url"]}

@app.post("/generate_url", tags=["url"])
async def generate_url(request: GenerateUrlRequest):
    encryption_handler = EncryptionHandler(request.api_password) if request.api_password else None
    query_params = request.query_params.copy()
    if "api_password" not in query_params and request.api_password:
        query_params["api_password"] = request.api_password
    ip_str = str(request.ip) if request.ip else None
    destination_url = request.destination_url
    if request.base64_encode_destination and destination_url:
        destination_url = encode_url_to_base64(destination_url)
    encoded_url = encode_mediaflow_proxy_url(
        mediaflow_proxy_url=request.mediaflow_proxy_url,
        endpoint=request.endpoint,
        destination_url=destination_url,
        query_params=query_params,
        request_headers=request.request_headers,
        response_headers=request.response_headers,
        encryption_handler=encryption_handler,
        expiration=request.expiration,
        ip=ip_str,
        filename=request.filename,
    )
    return {"url": encoded_url}

@app.post("/generate_urls", tags=["url"])
async def generate_urls(request: GenerateMultiUrlRequest):
    encryption_handler = EncryptionHandler(request.api_password) if request.api_password else None
    ip_str = str(request.ip) if request.ip else None

    async def _process_url_item(url_item: MultiUrlRequestItem) -> str:
        query_params = url_item.query_params.copy()
        if "api_password" not in query_params and request.api_password:
            query_params["api_password"] = request.api_password
        return encode_mediaflow_proxy_url(
            mediaflow_proxy_url=request.mediaflow_proxy_url,
            endpoint=url_item.endpoint,
            destination_url=url_item.destination_url,
            query_params=query_params,
            request_headers=url_item.request_headers,
            response_headers=url_item.response_headers,
            encryption_handler=encryption_handler,
            expiration=request.expiration,
            ip=ip_str,
            filename=url_item.filename,
        )

    tasks = [_process_url_item(url_item) for url_item in request.urls]
    encoded_urls = await asyncio.gather(*tasks)
    return {"urls": encoded_urls}

@app.post("/base64/encode", tags=["base64"])
async def encode_url_base64(url: str):
    try:
        encoded_url = encode_url_to_base64(url)
        return {"encoded_url": encoded_url, "original_url": url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to encode URL: {str(e)}")

@app.post("/base64/decode", tags=["base64"])
async def decode_url_base64(encoded_url: str):
    decoded_url = decode_base64_url(encoded_url)
    if decoded_url is None:
        raise HTTPException(status_code=400, detail="Invalid base64 encoded URL")
    return {"decoded_url": decoded_url, "encoded_url": encoded_url}

@app.get("/base64/check", tags=["base64"])
async def check_base64_url(url: str):
    is_base64 = is_base64_url(url)
    result = {"url": url, "is_base64": is_base64}
    if is_base64:
        decoded_url = decode_base64_url(url)
        if decoded_url:
            result["decoded_url"] = decoded_url
    return result

# Routers
app.include_router(proxy_router, prefix="/proxy", tags=["proxy"], dependencies=[Depends(verify_api_key)])
app.include_router(extractor_router, prefix="/extractor", tags=["extractors"], dependencies=[Depends(verify_api_key)])
app.include_router(speedtest_router, prefix="/speedtest", tags=["speedtest"], dependencies=[Depends(verify_api_key)])
app.include_router(playlist_builder_router, prefix="/playlist", tags=["playlist"])

# Static files
static_path = resources.files("mediaflow_proxy").joinpath("static")
app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")

# ✅ Final safe run() method
def run():
    import uvicorn
    import sys

    is_frozen = getattr(sys, 'frozen', False)

    if is_frozen:
        # Running as compiled .exe
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8888,
            log_level="info",
            workers=1,
            reload=False
        )
    else:
        # Running as script
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8888,
            log_level="info",
            workers=1,
            reload=True
        )

if __name__ == "__main__":
    run()
