from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from repositories.user_repository import UserRepository
from controllers.user_control import UserControl

from routes.sign_up_boundary import SignUpBoundary
from routes.sign_up_boundary import router as sign_up_router

from routes.admin_menu import AdminMenuBoundary
from routes.admin_menu import router as admin_router

user_repository = UserRepository()

user_control = UserControl(user_repository)

sign_up = SignUpBoundary(user_control)
admin = AdminMenuBoundary(user_control)

app = FastAPI()

app.include_router(sign_up_router)
app.include_router(admin_router)


@app.get("/", include_in_schema=False)
def root():
    """Redireciona para a documentação da API"""
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)