import os

from controllers.facade_singleton_controller import FacadeSingletonController
from repositories.repository_factory import get_repository_factory
from schema.user_schema import UserCreateSchema

# Limpa o arquivo legado para garantir teste limpo
if os.path.exists('legacy_users.json'):
    os.remove('legacy_users.json')

# Reseta o singleton entre execuções do script
FacadeSingletonController._instance = None

factory = get_repository_factory('legacy')
repo = factory.create_user_repository()
facade = FacadeSingletonController(repo)

# 1. Cadastra um usuário
payload = UserCreateSchema(
    name='João',
    email='joao@example.com',
    user_type='user',
    login='joao',
    phone='999',
    password='Senha123!'
)
created = facade.sign_up(payload)
print('Usuário cadastrado:', created.to_dict())

# 2. Lista usuários
listed = facade.list_users()
print('Usuários após cadastro:', [u.to_dict() for u in listed])

# 3. Simula reinício: novo singleton com novo repositório
FacadeSingletonController._instance = None
factory2 = get_repository_factory('legacy')
repo2 = factory2.create_user_repository()
facade2 = FacadeSingletonController(repo2)

listed2 = facade2.list_users()
print('Usuários após reiniciar:', [u.to_dict() for u in listed2])

# 4. Histórico de comandos
print('Histórico do command bus:', facade2.command_history())
