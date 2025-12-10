from fastapi import APIRouter, HTTPException, status
from typing import List
from models.user import User, TipoUsuario
from schema.user_schema import UserCreateSchema, UserResponseSchema

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


usuarios_db: List[User] = [] # armazenamento dos usuários "Banco de dados"
contador_id = 0 # id para cada usuário (vai ser incrementado a cada novo usuário)


@router.post("/", response_model=UserResponseSchema)
def adicionar_usuario(user_data: UserCreateSchema):
    """
    Adiciona um novo usuário ao sistema.
    
    - nome: Nome completo do usuário
    - email: Email válido do usuário
    - tipo: Tipo do usuário (vendedor ou cliente)
    - telefone: Telefone do usuário (opcional)
    """
    global contador_id
    
    #verifica se o email já existe
    for user in usuarios_db:
        if user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user_data.email} já cadastrado"
            )
    
    # Cria novo usuário
    contador_id += 1
    tipo = TipoUsuario.VENDEDOR if user_data.tipo.value == "vendedor" else TipoUsuario.CLIENTE
    
    novo_usuario = User(
        id=contador_id,
        nome=user_data.nome,
        email=user_data.email,
        tipo=tipo,
        telefone=user_data.telefone
    )
    
    # armazea na lista
    usuarios_db.append(novo_usuario)
    
    return novo_usuario.to_dict()


@router.get("/", response_model=List[UserResponseSchema])
def listar_usuarios():
    """
    Lista todos os usuários cadastrados no sistema.
    
    Retorna uma lista com todos os usuários (vendedores e clientes) armazenados em memória.
    """
    return [user.to_dict() for user in usuarios_db]


@router.get("/{user_id}", response_model=UserResponseSchema)
def buscar_usuario(user_id: int):
    """
    Busca um usuário específico pelo ID.
    
    - user_id: ID do usuário a ser buscado
    """
    for user in usuarios_db:
        if user.id == user_id:
            return user.to_dict()
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Usuário com ID {user_id} não encontrado"
    )


@router.get("/tipo/{tipo_usuario}", response_model=List[UserResponseSchema])
def listar_usuarios_por_tipo(tipo_usuario: str):
    """
    Lista usuários filtrados por tipo.
    
    - tipo_usuario: Tipo de usuário para filtrar (vendedor ou cliente)
    """
    if tipo_usuario not in ["vendedor", "cliente"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo inválido. Use 'vendedor' ou 'cliente'"
        )
    
    usuarios_filtrados = [
        user.to_dict() for user in usuarios_db 
        if user.tipo.value == tipo_usuario
    ]
    
    return usuarios_filtrados
