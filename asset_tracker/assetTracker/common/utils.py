# Utility functions file.
import datetime
import uuid
from dateutil import tz

def convert_datetime_to_string(datetime_obj, format="%d-%m-%Y %H:%m"):
    """
    This method is used to convert string object to the given format with local timezone.
    Args:
        datetime_obj: String object
        format: output format
    Returns:
        converted string object.
    """
    to_zone = tz.gettz("Asia/Kolkata")
    datetime_obj = datetime.datetime.strptime(datetime_obj, "%Y-%m-%dT%H:%M:%S.%fZ")
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