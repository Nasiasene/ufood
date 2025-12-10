from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.user_routes import router as user_router

app = FastAPI()

app.include_router(user_router)


@app.get("/", include_in_schema=False)
def root():
    """Redireciona para a documentação da API"""
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)