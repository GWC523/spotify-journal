import os

class Config:
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    TOKEN_INFO = "token_info"
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    TICKET_MASTER_API_KEY = os.getenv('TICKET_MASTER_API_KEY')
