# Utility functions file.
import datetime
import uuid

def convert_datetime_to_string(datetime_obj, format="%d-%m-%Y %H:%m"):
    """
    This method is used to convert datetime object to string in the given format.
    Args:
        datetime_obj: Datetime object
        format: output format
    Returns:
        converted string object.
    """
    return datetime.datetime.strftime(datetime_obj, format)

def get_uuid():
    """
    This method is used to generate UUID string.
    Args:
        None
    Return:
        UUID String.
    """
    return uuid.uuid4()