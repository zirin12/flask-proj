import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.sqlite3'

    @classmethod
    def init_app(cls, app):

        #log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite3'

    @classmethod
    def init_app(cls, app):
        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'production' : ProductionConfig,
    'testing' : TestingConfig,
    'default' : DevelopmentConfig
}