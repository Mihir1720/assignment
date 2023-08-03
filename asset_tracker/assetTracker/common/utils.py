# Utility functions file.
import datetime
import uuid
from dateutil import tz

def convert_datetime_to_string(datetime_obj, format="%d-%m-%Y %H:%m"):
    """
    This method is used to convert datetime object to string in the given format.
    Args:
        datetime_obj: Datetime object
        format: output format
    Returns:
        converted string object.
    """
    to_zone = tz.gettz("Asia/Kolkata")
    datetime_obj = datetime_obj.astimezone(to_zone)
    return datetime.datetime.strftime(datetime_obj, format)

def get_uuid():
    """
    This method is used to generate UUID string.
    Args:
        None
    Return:
        UUID string.
    """
    return str(uuid.uuid4())