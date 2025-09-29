import uvicorn
from src.config import settings


def start_api_server():
    uvicorn.run(
        "src.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        workers=1,
        forwarded_allow_ips="*",
        proxy_headers=True,
    )


if __name__ == "__main__":
    start_api_server()
