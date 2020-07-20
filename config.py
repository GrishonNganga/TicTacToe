class Config:
    '''
    General configparent class
    '''
    pass
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