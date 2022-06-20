import json

def get_bot_token():
    config_file = open('config.json')
    config_data = json.load(config_file)
    print(config_data)