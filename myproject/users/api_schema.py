from ninja import Schema


class RegisterIn(Schema):
    """注册入参"""
    username: str
    password: str
    confirm_password: str


class LoginIn(Schema):
    username: str
    password: str

class TokenIn(Schema):
    token:str

class TokenOut(Schema):
    username:str

class UserOut(Schema):
    id:int
    username:str
    is_active:int