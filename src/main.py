from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from repositories.user_repository import InMemoryUserRepository, SqliteUserRepository
from controllers.facade_singleton_controller import FacadeSingletonController

from routes.sign_up_boundary import SignUpBoundary
from routes.sign_up_boundary import router as sign_up_router

from routes.admin_menu import AdminMenuBoundary
from routes.admin_menu import router as admin_router

# "memory" = in-RAM (lost on restart) | "sqlite" = persisted to local database
STORAGE_MODE = "sqlite"

if STORAGE_MODE == "sqlite":
    from repositories.database import init_db
    init_db()
    user_repository = SqliteUserRepository()
else:
    user_repository = InMemoryUserRepository()

# Inicializa o Facade com o repositório escolhido
facade = FacadeSingletonController(user_repository)

# Acessa o UserControl através do Facade, usando sempre a mesma instância do controller
user_control = facade.user_control 

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