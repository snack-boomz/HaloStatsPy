import requests

from instance.instance import Halo_instance



if __name__ == "__main__":
    
    loop = True
    while loop:

        new_instance = Halo_instance("Slayter J")
        print(new_instance.__str__())
        
        #new_instance.generate_auth_url(client_id, client_secret)
        
        client_id = input(f"Please enter your Azure-provided client_id: ")
        client_secret = input(f"Please enter your Azure-provided client secret: ")
        new_instance.create(client_id, client_secret)
        
        
        
        loop = False

