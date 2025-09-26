import yaml
import os


def deep_update(original, update):
    for key, value in update.items():
        if isinstance(value, dict) and key in original:
            deep_update(original[key], value)
        else:
            original[key] = value


def load_env_config(default_cfg, env_name):
    cfg = default_cfg.copy()
    # 使用相对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '', f'{env_name}_config.yml')
    with open(config_path, 'r', encoding='utf-8') as file:
        dev_config = yaml.safe_load(file)
        deep_update(cfg, dev_config)
    return cfg


def load_default_config():
    # 使用相对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '', 'config.yml')
    with open(config_path, 'r', encoding='utf-8') as file:
        cfg = yaml.safe_load(file)
        cfg = load_env_config(cfg, cfg['ENV'])
    return cfg


CONFIG = load_default_config()