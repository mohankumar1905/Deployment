from flask import Flask
from api.config import get_logger

_logger = get_logger(logger_name=__name__)

def create_app(*, config_object) -> Flask:
    """Create a flask app instance. Usually we will create the  
    flask object it with __name__ when calling in a main function""" 
    
    flask_app = Flask('ml_api')
    flask_app.config.from_object(config_object)

    #Instead of giving app.route we can configire blueprint 
    #import blueprints
    from api.controller import prediction_app
    flask_app.register_blueprint(prediction_app)
    _logger.debug('Application instance created')

    return flask_app
