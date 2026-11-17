from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB
users = db.users

user_list = [
    {
    "name":"Homer Simpson",
    "username":"homer",
    "password":"homer_s",
    "email":"homer@com661.com",
    "admin":False
    },
    {
    "name":"Simpson",
    "username":"simp",
    "password":"simp_s",
    "email":"simp@com661.com",
    "admin":True
    },
    {
    "name":"Lisa simpson",
    "username":"Lisa",
    "password":"Lisa_s",
    "email":"Lisa@com661.com",
    "admin":False
    }
]
# pip install bcrypt
for new_user in user_list:
    new_user["password"] = bcrypt.hashpw(
        new_user["password"].encode('utf-8'),
        bcrypt.gensalt()
    )
    users.insert_one(new_user)