import requests
import webbrowser
from colorama import Fore
import json


class Halo_instance():
    pass

    def __init__(self, username):
        self.username = username
        
    def __str__(self):
        return self.username
        
    def create(self, client_id, client_secret):
        #self.generate_auth_url(client_id, client_secret)
        self.generate_auth_url(client_id)
        auth_code = input("After authenticating with microsoft using your provided client ID, please paste the auth code that was attached as a query parameter in the browser:  ")
        self.request_oauth_token(client_id, client_secret, auth_code)
        
    def generate_auth_url(self, client_id):
        
        # https://www.geeksforgeeks.org/python-script-to-open-a-web-browser/
        # https://www.csestack.org/code-python-to-open-url-in-browser/
        
        data = {
            'client_id': f'{client_id}',
            'response_type': 'code',
            'approval_prompt': 'auto',
            'scope': ["Xboxlive.signin", "Xboxlive.offline_access"],
            'redirect_uri': 'https://localhost',
            'state': 3903784
        }
        
        # https://www.geeksforgeeks.org/python-extract-key-value-of-dictionary-in-variables/
        # https://www.geeksforgeeks.org/python-accessing-key-value-in-dictionary/
        # https://www.geeksforgeeks.org/python-dictionary-keys-method/
        # https://stackoverflow.com/questions/18552001/accessing-dict-keys-element-by-index-in-python3
        
        params = list(data)
        
        client_id_param = params[0]
        client_id_value = data["client_id"]
        
        response_type_param = params[1]
        response_type_value = data["response_type"]
        
        approval_prompt_param = params[2]
        approval_prompt_value = data["approval_prompt"]
        
        scope_param = params[3]
        scope_value = f'{data["scope"][0]}+{data["scope"][1]}'
        
        redirect_uri_param = params[4]
        redirect_uri_value = data["redirect_uri"]
        
        state_param = params[5]
        state_value = data["state"]
        
        auth_url = f"https://login.live.com/oauth20_authorize.srf?{client_id_param}={client_id_value}&{response_type_param}={response_type_value}&{approval_prompt_param}={approval_prompt_value}&{scope_param}={scope_value}&{redirect_uri_param}={redirect_uri_value}"
        
        # https://www.geeksforgeeks.org/python-script-to-open-a-web-browser/
        # https://www.csestack.org/code-python-to-open-url-in-browser/
        
        webbrowser.get('safari').open_new(auth_url)
        
        #auth_response = requests.get(auth_url, params=data, verify=True)
        #print(auth_response)
        #print(auth_response.text)
        
    def request_oauth_token(self, client_id, client_secret, auth_code):
        
        #https://stackoverflow.com/questions/44964529/how-to-send-urlencoded-parameters-in-post-request-in-python
        
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'approval_prompt': 'auto',
            'scope': 'Xboxlive.signin,Xboxlive.offline_access',
            'redirect_uri': 'https://localhost',
            'client_id': client_id,
            'client_secret': client_secret
        }
        
        oauth_url = f"https://login.live.com/oauth20_token.srf"
        oauth_response = requests.post(oauth_url, data=data)
        oauth_response_json = oauth_response.json()
        # https://www.geeksforgeeks.org/print-colors-python-terminals/
        
        if '200' in str(oauth_response.status_code):
            print(Fore.GREEN + "\nSuccess!" + Fore.RESET)
        else:
            print(Fore.RED + "\nFailed!" + Fore.RESET)
        
        
        # https://stackoverflow.com/questions/53175422/formatting-json-in-python
        
        pretty_oauth_response = json.dumps(oauth_response.json(), indent=4)
        
        print(f"\n\n{pretty_oauth_response}")
        print(f'Access Token: {oauth_response_json["access_token"]}')
        
        
    def request_user_token():
        pass
    