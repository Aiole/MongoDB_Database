import pymongo

#Setup creating DB and connecting to Mongo
from pymongo import MongoClient
client = MongoClient()

client = MongoClient('localhost', 27017)


db = client.ytla
test_database = db.test_database

#Retrieval

print("Please select a search method: 'Between', 'UptoPresent', ...") 


#Accepting inputs in proper timestamp format
print('Insert the start time you are looking for: ')
start_time = input()
print('Insert the end time you are looking for: ')
end_time = input()


#Sets the greater than or equal to and less than or equal to parameters with regards to start and end time
gtequery = { "timestamp": { "$gte": start_time, "$lte": end_time } }

#Searches database with those parameters
gteresult = test_database.find(gtequery)

#Prints all the results found
for x in gteresult:
	print(x)
