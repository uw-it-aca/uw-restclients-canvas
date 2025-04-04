from uw_canvas.developer_keys import DeveloperKeys
from commonconf.backends import use_configparser_backend
from commonconf import settings
import os


def get_developer_keys(id=None):
    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'settings.cfg')
    use_configparser_backend(settings_path, 'Canvas')

    account_id = getattr(settings, 'RESTCLIENTS_CANVAS_ACCOUNT_ID')
    params = {'per_page': 100}

    canvas = DeveloperKeys()
    
    if id:
        developer_key = canvas.get_developer_key_by_id(id)
        print(f"{developer_key['name']}: {developer_key['id']}")
        return developer_key
    else:
        for key in canvas.get_developer_keys():
            print(f"{key['name']}: {key['id']}")

def update_developer_key(developer_key_id, json_data):
    """
    Update the developer key identified by developer_key_id with the
    given json data.
    """
    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'settings.cfg')
    use_configparser_backend(settings_path, 'Canvas')

    account_id = getattr(settings, 'RESTCLIENTS_CANVAS_ACCOUNT_ID')
    canvas = DeveloperKeys()
    return canvas.update_developer_key(developer_key_id, json_data)

if __name__ == '__main__':

    # Example GET request to list developer keys
    get_developer_keys()

    # Example GET request to get a specific developer key by ID
    # get_developer_keys(KEY_ID)

    # Example request to update developer key
    # Note: API docs indicate redirect_uris should be an array, but in practice
    # it needs to be a single newline delminited string.
    # callbacks = ['https://example.com/callback1',
    #             'https://example.com/callback2',
    #             'https://example.com/callback3']
    # stringified_values = "\n".join(callbacks)
    # payload = {
    #     "developer_key": {
    #         "redirect_uris": stringified_values
    #     }
    # }
    # update_developer_key(100000000000386, payload)
