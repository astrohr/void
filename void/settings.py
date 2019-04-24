import os
from pathlib import Path

from dotenv import load_dotenv


class Settings:
    _loaded = False

    defaults = {
        'POSTGRES_USER': 'void',
        'POSTGRES_PASSWORD': 'void',
        'POSTGRES_DB': 'void',
        'POSTGRES_PORT': 5433,
    }

    rc_str = str(Path.home() / '.voidrc')

    def load(self, env_file=rc_str):
        if not self._loaded:
            load_dotenv(env_file, verbose=True)
            self._loaded = True

    def __getattr__(self, item):
        if not self._loaded:
            raise RuntimeError('Settings not yet loaded.')
        return os.getenv(item, self.defaults.get(item))


settings = Settings()
