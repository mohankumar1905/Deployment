from api.app import create_app
from api.config import DevelopmentConfig

application = create_app(config_object=DevelopmentConfig)

if __name__ == '__main__':
    """ __name__ will __main__ for the python scripts we execute directly.
For the callable scripts (It will be the script and the function name we called.)"""
    #Runs the Flask App object that returns
    application.run()