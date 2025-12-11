from models.user import User

class UserRepository:
    def __init__(self):
        self.users = []
        self.contador_id = 0
    
    def add(self, user: User) -> User:
        self.contador_id +=1
        user.id = self.contador_id
        self.users.append(user)
        
        return user
    
    def list_users(self):
        return self.users
    