# Chat Bot user details will be stored in an event of an emergency situation 
    
class UserProfile:
    def __init__(self, name: str = None, phone: str = None, age: int = 0):
        self.name = name
        self.phone = phone
        self.age = age
        