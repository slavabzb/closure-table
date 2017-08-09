import yaml


def load_conf(path):
    with open(path, "r") as fp:
        return yaml.safe_load(fp)
