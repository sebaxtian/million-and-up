import uvicorn

if __name__ == "__main__":
    """Running microservice"""
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8001,
        log_level="info",
        reload=True,
        workers=1,
    )
