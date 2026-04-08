from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from repositories.repository_factory import get_repository_factory
from controllers.facade_singleton_controller import FacadeSingletonController

from observers.user_deletion_observer import DeletionLogObserver, ScheduledDeletionObserver
from routes.admin_menu import AdminMenuBoundary
from routes.admin_menu import router as admin_router
from routes.delete_user_boundary import DeleteUserBoundary
from routes.delete_user_boundary import router as delete_user_router
from routes.edit_user_boundary import EditUserBoundary
from routes.edit_user_boundary import router as edit_user_router
from routes.sign_up_boundary import SignUpBoundary
from routes.sign_up_boundary import router as sign_up_router

# "memory" = in-RAM (lost on restart) | "sqlite" = persisted to local database
STORAGE_MODE = "sqlite"

# Obtém a factory apropriada
repository_factory = get_repository_factory(STORAGE_MODE)

# Inicializa banco de dados se usando SQLite
if STORAGE_MODE == "sqlite":
    from repositories.database import init_db
    init_db()

# Cria os repositórios através da factory
user_repository = repository_factory.create_user_repository()

# Inicializa o Facade com o repositório escolhido
facade = FacadeSingletonController(user_repository)

facade.subscribe_deletion_observer(DeletionLogObserver())
facade.subscribe_deletion_observer(ScheduledDeletionObserver())

sign_up = SignUpBoundary(facade)
admin = AdminMenuBoundary(facade)
edit_user = EditUserBoundary(facade)
delete_user = DeleteUserBoundary(facade)

app = FastAPI()

app.include_router(sign_up_router)
app.include_router(edit_user_router)
app.include_router(delete_user_router)
app.include_router(admin_router)


@app.get("/", include_in_schema=False)
def root():
    """Redireciona para a documentação da API"""
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)