# ufood

## Descrição

Marketplace interno para vendas no CI/UFPB. Sistema desenvolvido para a disciplina de métodos de projeto de software.

## Estrutura de Pastas

```
src/
├── main.py          # Aplicação FastAPI
├── requirements.txt # Dependências
├── models/          # Classes de domínio
├── schema/          # Validação de dados
└── routes/          # Endpoints da API
```

## Como Utilizar

### Executar servidor

```bash
cd src
python3 main.py
```

Servidor disponível em: `http://localhost:8000`

Documentação: `http://localhost:8000/docs`

### Requisições

**POST /usuarios/** - Adicionar usuário

```bash
curl -X POST "http://localhost:8000/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@email.com",
    "tipo": "cliente",
    "telefone": "11999999999"
  }'
```

**GET /usuarios/** - Listar todos

```bash
curl "http://localhost:8000/usuarios/"
```

**GET /usuarios/{id}** - Buscar por ID

```bash
curl "http://localhost:8000/usuarios/1"
```
