from .var import access_token_BD, database_name
from pymongo import MongoClient
conn = MongoClient(
    "mongodb+srv://yess:"+access_token_BD+"@cluster0.wdzh1o3.mongodb.net/?retryWrites=true&w=majority")[database_name]
