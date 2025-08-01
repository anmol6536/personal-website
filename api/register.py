import pkgutil
import importlib
from flask import Flask

def register_blueprints(app: Flask, package_name: str):
    package = importlib.import_module(package_name)
    for _, name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f'{package_name}.{name}')
        for item in dir(module):
            if item.endswith('_bp'):
                bp = getattr(module, item)
                app.register_blueprint(bp) 