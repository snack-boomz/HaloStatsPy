"""This module....

Returns:
    _type_: _description_
"""

__version__ = "0.1"
__author__ = "snack_boomz"

from colorama import Fore

from logging_class.log import Log

from collections import OrderedDict
import requests
import webbrowser
import json



class Halo_instance():

    def __init__(self, username, client_id, client_secret):
        self.username = username
        self.logger = ""
        self.log_level = 0
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_code = ""
        self.oauth_token = ""
        self.user_hash = ""
        self.user_token = ""
        self.xsts_token = ""
        self.spartan_token = ""
        self.spartan_clearance = ""
        
    def __str__(self):
        return self.username, self.auth_code, self.oauth_token, self.user_token, self.xsts_token, self.spartan_token, self.spartan_clearance
        
    def create(self):
        #self.generate_auth_url(client_id, client_secret)
        
        log_levels = OrderedDict([
            ('0', 0),
            ('1', 1),
            ('91', 91)
        ])
        
        log_level_descriptions = OrderedDict([
            ('0', 'Logging Disabled'),
            ('1', 'Normal (default) logging level'),
            ('91', 'Most Detailed logging level')
        ])
        
        try:
            
            print("\n Press 'q' to quit.\n")
            for key, value in log_levels.items():
                print(f'{key}) {log_level_descriptions[key]}')
            choice = input(f'\n"Choose a log level: ').strip()
            
            #if choice in log_levels:
            self.logger = Log(1)
            print(self.logger)
            #elif choice == 'q':
            #    quit()
            #else:
            #    raise ValueError("That isn't a valid menu option. Please try again.")
            
        except ValueError as err:
            print("Input invalid.")
            print(f'Error: {err}')
        
        self.generate_auth_url(self.client_id, self.logger)
        
        self.auth_code = input("After authenticating with microsoft using your provided client ID, please paste the auth code that was attached as a query parameter in the browser:  ")
        
        self.oauth_token = self.request_oauth_token(self.client_id, self.client_secret, self.auth_code, self.logger)
        
        self.user_hash, self.user_token = self.request_user_token(self.client_id, self.client_secret, self.auth_code, self.oauth_token, self.logger)
        
          
        
    def generate_auth_url(self, client_id, logger):
        """_summary_

        Args:
            client_id (_type_): _description_
            logger (_type_): _description_
        """
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
        
    def request_oauth_token(self, client_id, client_secret, auth_code, logger):
        """_summary_

        Args:
            client_id (_type_): _description_
            client_secret (_type_): _description_
            auth_code (_type_): _description_
            logger (_type_): _description_

        Returns:
            oauth_token (_type_): _description_
        """
        
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
            logger.print(Fore.GREEN + "\nSuccess!" + Fore.RESET, 0)
        else:
            logger.print(Fore.RED + "\nFailed!" + Fore.RESET, 0)
        
        
        # https://stackoverflow.com/questions/53175422/formatting-json-in-python
        
        pretty_oauth_response = json.dumps(oauth_response.json(), indent=4)
        
        print(f"\n\n{pretty_oauth_response}")
        print(f'Access Token: {oauth_response_json["access_token"]}')
        oauth_token = oauth_response_json["access_token"]
        
        return oauth_token
        
        
    def request_user_token(self, client_id, client_secret, auth_code, oauth_token, logger):
        dictionary = {
            'Properties': {
                'AuthMethod': 'RPS',
                'RpsTicket': f'd={oauth_token}',
                'SiteName': 'user.auth.xboxlive.com'
                }, 
            'RelyingParty': 'http://auth.xboxlive.com',
            'TokenType': 'JWT'
        }
        
        print(self.__str__())
        json_string = json.dumps(dictionary, indent=4)
        
        user_token_url = f"https://user.auth.xboxlive.com/user/authenticate"
        user_token_response = requests.post(user_token_url, json=dictionary)
        user_token_response_json = user_token_response.json()
        # https://www.geeksforgeeks.org/print-colors-python-terminals/
        
        if '200' in str(user_token_response.status_code):
            logger.print(Fore.GREEN + "\nSuccess!" + Fore.RESET, 0)
        else:
            logger.print(Fore.RED + "\nFailed!" + Fore.RESET, 0)
            
        pretty_user_token_response = json.dumps(user_token_response.json(), indent=4)
        
        print(f"\n\n{pretty_user_token_response}")
        print(f'User Hash: {user_token_response_json["DisplayClaims"]["xui"][0]}')
        print(f'User Token: {user_token_response_json["Token"]}')
        
        #https://datagy.io/python-return-multiple-values/
        
        user_hash = user_token_response_json["DisplayClaims"]["xui"][0]["uhs"]
        user_token = user_token_response_json["Token"]
        
        return user_hash, user_token
        
        
        
    