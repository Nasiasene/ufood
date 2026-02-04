class ValidationException(Exception):
    """Exceção lançada para violações de regras de negócio (Login/Senha)."""
    ## classe foi criada para tratar a regra de negócio de validação de login e senha no schema do usuário
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)