import os
import json


with open("run_conf.json", "r") as f:
    config = json.load(f)

if config["needs_poetry"]:
    os.system("pip install poetry")
    config["needs_poetry"] = False

if config["needs_packages"]:
    os.system("poetry install")
    config["needs_packages"] = False

if any(config.values()):
    json.dump(config, open("run_conf.json", "w"), indent=4)


os.system("poetry run python -m project_ripple.Main")