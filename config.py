import os

class Config:
    '''
    General configparent class
    '''
    API_KEY=os.environ.get('API_KEY')
    SECRET_KEY=os.environ.get('SECRET_KEY')
    # Database config
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://miro:password@localhost/andika' 

class ProdConfig(Config):
    pass

class DevConfig(Config):
    Debug = True

config_options = {
    'development': DevConfig,
    'production': ProdConfig,
}