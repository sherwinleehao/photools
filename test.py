import json

print("Load Settings")
path = 'Temp/Settings.json'
settingsStr = open(path, 'r').read()
print(settingsStr)

settings = json.loads(settingsStr)
# print(settings)