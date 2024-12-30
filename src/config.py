import json

class Config:
    def __init__(self, config_path = './config.json'):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_path, encoding='utf-8') as f:
            return json.load(f)

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value

    def __delitem__(self, key):
        del self.config[key]

    def __iter__(self):
        return iter(self.config)

    def __len__(self):
        return len(self.config)

    def __str__(self):
        return str(self.config)

    def __repr__(self):
        return repr(self.config)

    def __contains__(self, key):
        return key in self.config

    def items(self):
        return self.config.items()

    def keys(self):
        return self.config.keys()

    def values(self):
        return self.config.values()

    def save(self):
        json_str = json.dumps(self.config, indent=4)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            f.write(json_str)