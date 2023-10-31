import yaml


def deep_update(original, update):
    for key, value in update.items():
        if isinstance(value, dict) and key in original:
            deep_update(original[key], value)
        else:
            original[key] = value


def load_env_config(default_cfg, env_name):
    cfg = default_cfg.copy()
    with open(f'config/{env_name}_config.yml', 'r', encoding='utf-8') as file:
        dev_config = yaml.safe_load(file)
        deep_update(cfg, dev_config)
    return cfg


def load_default_config():
    with open('config/config.yml', 'r', encoding='utf-8') as file:
        cfg = yaml.safe_load(file)
        cfg = load_env_config(cfg, cfg['ENV'])
    return cfg


CONFIG = load_default_config()
