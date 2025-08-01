from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.patterns.singleton import Singleton

class SqlManager(metaclass=Singleton):
    def __init__(self):
        self._engines = {}
        self._sessions = {}

    def add_engine(self, name, url):
        if name in self._engines:
            return self._engines[name]
            
        engine = create_engine(url)
        self._engines[name] = engine
        Session = sessionmaker(bind=engine)
        self._sessions[name] = Session
        return engine

    def get_engine(self, name):
        return self._engines.get(name)

    def get_session(self, name):
        Session = self._sessions.get(name)
        return Session() if Session else None

def setup_sqlite_from_config(config_path='config.yaml'):
    import yaml
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    db_path = config.get('database', {}).get('path')
    if db_path:
        db_url = f'sqlite:///{db_path}'
        sql_manager = SqlManager()
        sql_manager.add_engine('default', db_url)
    else:
        raise ValueError("Database path not found in config.yaml") 