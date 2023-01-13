class Production(object):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False
    SECRET_KEY = '1234'
    SQLALCHEMY_DATABASE_URI = "sqlite:///storage.db"    

class Development(Production):
    DEBUG = True
    DEVELOPMENT = True
    TESTING = True


