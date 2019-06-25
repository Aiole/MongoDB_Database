print('Insert the time you are looking for: ')
input_time = input()
find_data = test_database.find_one({'timestamp': input_time})
print(find_data)
