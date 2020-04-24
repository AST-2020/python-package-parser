import json

data = {}
data['car'] = {}
data['car']['1'] = ({
    'brand': 'Toyota',
    'model': 'Supra',
    'performance':{
        'horsepower': 600,
        'torque': 1000
    }
})
data['car']['2'] = ({
    'brand': 'Porsche',
    'model': '911',
    'performance':{
        'horsepower': 500,
        'torque': 900
    }
})
data['truck'] = {}



with open('example.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
print("Data saved to the json file.")

with open('example.json') as inputfile:
    input = json.load(inputfile)

print(input['car']['1'])
