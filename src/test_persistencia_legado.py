from repositories.repository_factory import get_repository_factory
from controllers.facade_singleton_controller import FacadeSingletonController
from schema.user_schema import UserCreateSchema
import os

# Limpa o arquivo legado para o teste
if os.path.exists('legacy_users.json'):
    os.remove('legacy_users.json')

# Use o adapter (sistema legado)
factory = get_repository_factory('legacy')
repo = factory.create_user_repository()
facade = FacadeSingletonController(repo)
control = facade.user_control

# 1. Cadastra um usuário
payload = UserCreateSchema(
    name='João',
    email='joao@example.com',
    user_type='user',
    login='joao',
    phone='999',
    password='Senha123!'
)
created = control.sign_up(payload)
print('Usuário cadastrado:', created.to_dict())

# 2. Lista usuários (deve aparecer o João)
listed = control.list_users()
print('Usuários após cadastro:', [u.to_dict() for u in listed])

# 3. Reinicia o programa (simulado)
# Cria novo controle, que recarrega do arquivo
factory2 = get_repository_factory('legacy')
repo2 = factory2.create_user_repository()
facade2 = FacadeSingletonController(repo2)
control2 = facade2.user_control

listed2 = control2.list_users()
print('Usuários após reiniciar:', [u.to_dict() for u in listed2])
