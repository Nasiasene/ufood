from controllers.user_control import UserControl
from repositories.user_repository import UserRepository

#Aplicação do Padrão Facade + Singleton para centralizar o acesso aos controllers
#e garantir uma única instância do Facade durante a execução da aplicação.
class FacadeSingletonController:
    _instance = None

    def __new__(cls, user_repository: UserRepository):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_once(user_repository)
        return cls._instance

    def _init_once(self, user_repository: UserRepository):
        # registro de controllers do sistema
        self._user_control = UserControl(user_repository)
        

    @property
    def user_control(self) -> UserControl:
        return self._user_control

    def count_entities(self) -> int:
        # Contar o número total de entidades gerenciadas pelos controllers
        return len(self._user_control.list_users())