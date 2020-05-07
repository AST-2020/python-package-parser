import json

# file to read our saved data from the json file
with open('resultsPytorch.txt') as json_file:
    data = json.load(json_file)

print(data)