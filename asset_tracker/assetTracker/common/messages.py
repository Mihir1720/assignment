# Message manager file.
# We can store project wide messages here and use them as and when required.
def get_message(message):
    """
    This method is used to get message from a mapping.
    Args:
        message: String(message flag/identifier)
    Returns:
        message text.
    """
    mapping = {
        "LOGIN_SUCCESSFUL": "Login successful.",
        "LOGIN_FAILED": "Login failed.",
        "LOGOUT_SUCCESSFUL": "Logout successful.",
        "INVALID_HOST": "Access from this host is not allowed.",
        "NO_ASSET_TYPES_FOUND": "No asset types found.",
        "ASSET_TYPE_ADD_SUCCESSFUL": "Asset type added successfully.",
        "INVALID_ASSET_TYPE": "Please select a valid asset type.",
        "ASSET_TYPE_UPDATE_SUCCESSFUL": "Asset type updated successfully.",
        "ASSET_TYPE_DELETE_SUCCESSFUL": "Asset type deleted successfully.",
        "NO_ASSETS_FOUND": "No assets found.",
        "ASSET_ADD_SUCCESSFUL": "Asset added successfully.",
        "INVALID_ASSET": "Please select a valid asset.",
        "ASSET_UPDATE_SUCCESSFUL": "Asset updated successfully.",
        "ASSET_DELETE_SUCCESSFUL": "Asset deleted successfully.",
        "SOMETHING_WENT_WRONG": "Something went wrong.",
        "INVALID_PAGE_NUMBER": "Incorrect page number."
    }
    return mapping.get(message, message)