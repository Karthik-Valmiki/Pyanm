import sys
import uvicorn

if __name__ == "__main__":
    reload_mode = "--reload" in sys.argv
    print("Pyanm: Network Flow & Bot Intrusion Detection Platform")
    print()
    print("Web Dashboard:  http://127.0.0.1:8000/dashboard")
    print("API Docs:       http://127.0.0.1:8000/docs")
    print("ReDoc:          http://127.0.0.1:8000/redoc")
    print(f"Server Mode:    {'Hot Reloading (--reload)' if reload_mode else 'Standard (Windows-safe single process)'}")
    print()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=reload_mode)
