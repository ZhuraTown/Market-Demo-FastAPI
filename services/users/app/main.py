import uvicorn
from app.config import settings

def start_api_server():
    import asyncio
    from app.db.create_database import create_database
    asyncio.run(create_database())
    uvicorn.run(
        "app.api:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=True,
        workers=1,
        forwarded_allow_ips='*',
        proxy_headers=True,
    )


if __name__ == "__main__":
    start_api_server()