import os

from dotenv import load_dotenv


class Settings:
    _loaded = False

    defaults = {
        'POSTGRES_USER': 'void',
        'POSTGRES_PASSWORD': 'void',
        'POSTGRES_DB': 'void',
    }

    def load(self, env_file='/Users/fran/.voidrc'):
        if not self._loaded:
            load_dotenv(env_file, verbose=True)
            self._loaded = True

    def __getattr__(self, item):
        if not self._loaded:
            raise RuntimeError('Settings not yet loaded.')
        return os.getenv(item, self.defaults.get(item))


settings = Settings()
