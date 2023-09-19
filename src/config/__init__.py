import os
import yaml

config_path = os.path.join(os.getcwd(), "config/config.yml")

with open(config_path, 'r') as file:
    CONFIG = yaml.safe_load(file)