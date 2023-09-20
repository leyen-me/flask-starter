import os
import yaml

if 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):
    config_path = os.path.join(os.getcwd(), "config/config.production.yml")
else:
    config_path = os.path.join(os.getcwd(), "config/config.yml")

with open(config_path, 'r') as file:
    CONFIG = yaml.safe_load(file)