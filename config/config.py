import os 
import json 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "configuracoes.txt")

def load_config() :
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)