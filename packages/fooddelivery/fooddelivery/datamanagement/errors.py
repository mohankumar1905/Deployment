class BaseError(Exception):
    """Base Package error"""
    
class InvalidModelInputError(BaseError):
    """Model Input Contains an error"""