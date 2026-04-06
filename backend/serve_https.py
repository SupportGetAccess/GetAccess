import uvicorn
import ssl

if __name__ == "__main__":
    ssl_config = {
        "ssl_certfile": "../frontend/cert.pem",
        "ssl_keyfile": "../frontend/key.pem",
    }
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8443,
        reload=False,
        **ssl_config
    )
