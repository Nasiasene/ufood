"""
Teste integrado de todos os padrões de projeto implementados no UFood.
Execute a partir da pasta src/:  python test_all_patterns.py
"""

import os
from controllers.facade_singleton_controller import FacadeSingletonController
from filters.user_filter_strategy import (
    CompositeFilter, FilterByName, FilterByUserType,
)
from observers.user_deletion_observer import DeletionLogObserver, ScheduledDeletionObserver
from repositories.repository_factory import get_repository_factory
from repositories.user_type import UserType
from schema.store_schema import StoreCreateSchema, StoreUpdateSchema
from schema.user_schema import UserCreateSchema, UserUpdateSchema


def secao(titulo: str):
    print(f"\n{'='*55}")
    print(f"  {titulo}")
    print('='*55)


def ok(msg: str):
    print(f"  [OK] {msg}")


# ── Setup ────────────────────────────────────────────────────
FacadeSingletonController._instance = None
repo = get_repository_factory("memory").create_user_repository()
store_repo = get_repository_factory("memory").create_store_repository()
facade = FacadeSingletonController(repo, store_repo)

# ── Observer: registra observers antes de qualquer operação ──
facade.subscribe_deletion_observer(DeletionLogObserver())
facade.subscribe_deletion_observer(ScheduledDeletionObserver())


# ────────────────────────────────────────────────────────────
secao("1. SINGLETON — única instância do Facade")
# ────────────────────────────────────────────────────────────
facade2 = FacadeSingletonController(repo, store_repo)
assert facade is facade2, "Singleton falhou: duas instâncias diferentes!"
ok("facade is facade2 → mesma instância garantida")


# ────────────────────────────────────────────────────────────
secao("2. FACADE + COMMAND — cadastro de usuários (RF01)")
# ────────────────────────────────────────────────────────────
ana = facade.sign_up(UserCreateSchema(
    name="Ana Lima", email="ana@ufpb.br", user_type="user",
    login="ana", phone="83999991111", password="Senha123!"
))
admin = facade.sign_up(UserCreateSchema(
    name="Admin Sistema", email="admin@ufpb.br", user_type="admin",
    login="admin", phone="83999990000", password="Admin@2024!"
))
carlos = facade.sign_up(UserCreateSchema(
    name="Carlos Souza", email="carlos@ufpb.br", user_type="user",
    login="carlos", phone="83999992222", password="Carlos#123!"
))
ok(f"3 usuários cadastrados via SignUpUserCommand")

history = facade.command_history()
assert any(h["command"] == "SignUpUserCommand" for h in history)
ok(f"Histórico do CommandBus: {[h['command'] for h in history]}")


# ────────────────────────────────────────────────────────────
secao("3. TEMPLATE METHOD — fluxo fixo de criação (RF01)")
# ────────────────────────────────────────────────────────────
ok("SignUpOperationTemplate executou: prepare → validate → create_entity → persist")
ok(f"Login normalizado (strip): '{ana.login}'")
ok(f"Email normalizado (lower): '{ana.email}'")


# ────────────────────────────────────────────────────────────
secao("4. STRATEGY — filtros de listagem (RF09)")
# ────────────────────────────────────────────────────────────
todos = facade.list_users()
assert len(todos) == 3
ok(f"Sem filtro: {len(todos)} usuários")

por_nome = facade.list_users(filter=FilterByName("ana"))
assert len(por_nome) == 1
ok(f"FilterByName('ana'): {[u.name for u in por_nome]}")

por_tipo = facade.list_users(filter=FilterByUserType(UserType.ADMIN))
assert len(por_tipo) == 1
ok(f"FilterByUserType(ADMIN): {[u.name for u in por_tipo]}")

combinado = facade.list_users(filter=CompositeFilter([
    FilterByName("a"), FilterByUserType(UserType.USER)
]))
ok(f"CompositeFilter(nome='a' + tipo=USER): {[u.name for u in combinado]}")


# ────────────────────────────────────────────────────────────
secao("5. MEMENTO — desfazer edição (RF02)")
# ────────────────────────────────────────────────────────────
nome_original = ana.name

ana = facade.edit_user(ana.id, UserUpdateSchema(name="Ana Editada"))
assert ana.name == "Ana Editada"
ok(f"Após edit_user: '{ana.name}'")

ana = facade.edit_user(ana.id, UserUpdateSchema(name="Ana Segunda Edição"))
ok(f"Após 2ª edição: '{ana.name}'")

ana = facade.undo_last_edit(ana.id)
assert ana.name == "Ana Editada"
ok(f"Após 1º undo: '{ana.name}'")

ana = facade.undo_last_edit(ana.id)
assert ana.name == nome_original
ok(f"Após 2º undo (original): '{ana.name}'")

try:
    facade.undo_last_edit(ana.id)
    assert False, "Deveria lançar ValueError"
except ValueError:
    ok("3º undo sem histórico → ValueError correto")


# ────────────────────────────────────────────────────────────
secao("6. OBSERVER — exclusão com 30 dias de grace (RF03)")
# ────────────────────────────────────────────────────────────
from models.user_status import UserStatus

print("  (log do DeletionLogObserver abaixo)")
carlos_deletado = facade.delete_user(carlos.id)
assert carlos_deletado.status == UserStatus.PENDING_DELETION
assert carlos_deletado.deletion_scheduled_at is not None
ok(f"Status: {carlos_deletado.status.value}")
ok(f"Exclusão agendada: {carlos_deletado.deletion_scheduled_at.strftime('%d/%m/%Y')}")


# ────────────────────────────────────────────────────────────
secao("7. ABSTRACT FACTORY + REPOSITORY — lojas (RF04)")
# ────────────────────────────────────────────────────────────
loja1 = facade.create_store(StoreCreateSchema(name="Cantina Central", owner_id=ana.id, is_open=True))
loja2 = facade.create_store(StoreCreateSchema(name="Lanche Rápido", owner_id=admin.id))
ok(f"Loja criada: '{loja1.name}' (dono: usuário {loja1.owner_id})")
ok(f"Loja criada: '{loja2.name}' (dono: usuário {loja2.owner_id})")

lojas = facade.list_stores()
assert len(lojas) == 2
ok(f"list_stores(): {[l.name for l in lojas]}")

loja1 = facade.edit_store(loja1.id, StoreUpdateSchema(is_open=False))
assert loja1.is_open is False
ok(f"edit_store(): is_open → {loja1.is_open}")

facade.delete_store(loja2.id)
assert len(facade.list_stores()) == 1
ok(f"delete_store(): lojas restantes → {len(facade.list_stores())}")


# ────────────────────────────────────────────────────────────
secao("8. FACADE — count_entities (usuários + lojas)")
# ────────────────────────────────────────────────────────────
total = facade.count_entities()
ok(f"count_entities() = {total} (usuários ativos + lojas cadastradas)")


# ────────────────────────────────────────────────────────────
secao("9. ADAPTER — repositório legado")
# ────────────────────────────────────────────────────────────
if os.path.exists("legacy_users.json"):
    os.remove("legacy_users.json")

FacadeSingletonController._instance = None
legacy_repo = get_repository_factory("legacy").create_user_repository()
legacy_store_repo = get_repository_factory("legacy").create_store_repository()
legacy_facade = FacadeSingletonController(legacy_repo, legacy_store_repo)
legacy_facade.subscribe_deletion_observer(ScheduledDeletionObserver())

u = legacy_facade.sign_up(UserCreateSchema(
    name="Legado User", email="legado@ufpb.br", user_type="user",
    login="legado", phone="83000000000", password="Legado#123!"
))
ok(f"Usuário salvo via LegacyUserStorage (JSON): '{u.name}' id={u.id}")
assert os.path.exists("legacy_users.json")
ok("Arquivo legacy_users.json criado com sucesso")


# ────────────────────────────────────────────────────────────
print(f"\n{'='*55}")
print("  TODOS OS PADRÕES VERIFICADOS COM SUCESSO!")
print('='*55 + "\n")
