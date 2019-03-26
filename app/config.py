import os


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "1Nrd2JFQIWAh3aa0q9zrN15www7Czc6Q")


class Production(Config):
    pass


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True


configuration = {
    "development": Development,
    "production": Production,
    "testing": Testing
}
