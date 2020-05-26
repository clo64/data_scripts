import json

readTest = open('framedata_1.json')
data = json.load(readTest)

print(data["1"][1][0][2])