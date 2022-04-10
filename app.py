import requests

from instance.instance import *



if __name__ == "__main__":
    loop = True
    while loop:

        xboxlive_gt = input("Please enter your Microsoft Xbox Live Gamertag: ")
        client_id = input(f"Please enter your Azure-provided client_id: ")
        client_secret = input(f"Please enter your Azure-provided client secret: ")

        new_instance = Halo_instance(xboxlive_gt, client_id, client_secret)
        print(new_instance.__str__())
        
        #new_instance.generate_auth_url(client_id, client_secret)
        
        
        new_instance.create()
        
        
        
        loop = False

