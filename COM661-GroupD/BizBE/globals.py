from pymongo import MongoClient

secret_key = 'mysecret'

#Mongo connection
client = MongoClient("mongodb://localhost:27017")
db = client.bizDB