
import pymongo


#Setup creating DB and connecting to Mongo
from pymongo import MongoClient
client = MongoClient()

client = MongoClient('localhost', 27017)


db = client.ytla
test_database = db.test_database

print('Insert the time you are looking for: ')
input_time = input()
find_data = test_database.find_one({'timestamp': input_time})
print(find_data)
