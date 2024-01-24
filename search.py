#!/usr/bin/env python3 
from google.cloud import domains_v1
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToDict  

# need to enable "Cloud DNS API"
# need to create a Service Account

project_id = "sandbox-282715"
location = f"projects/{project_id}/locations/global" 

client = None

def get_client():
    global client
    if (client is None):
        key_path = "secrets/sandbox-282715-f70e398cc87d.json"
        credentials = service_account.Credentials.from_service_account_file(key_path) 
        client = domains_v1.DomainsClient(credentials=credentials)
    return client



def search_domains(requested_domain):
    if requested_domain == None:
        raise TypeError("You need to pass a domain name to search for!")

    print("Searching for " + requested_domain)

    # Create a client
    client = get_client()

    # Initialize request argument(s)
    request = domains_v1.SearchDomainsRequest(
        query=requested_domain,
        location=location,
    )

    return client.search_domains(request=request)


def is_available(requested_domain):
    response = search_domains(requested_domain)
    response_dict = MessageToDict(response._pb)
    available = response_dict['registerParameters'][0]['availability']     
    return available == "AVAILABLE"  


def register_domain(requested_domain):
    # Create a client
    client = get_client() # domains_v1.DomainsClient()

    # be sure it's available
    if not is_available(requested_domain):
        raise ValueError(f"Requested domain '{requested_domain}' is not available!")

    phone = "+15125533529"
    email = "domains@kellerhome.com"
    dns_settings = domains_v1.types.DnsSettings.CustomDns(name_servers = ["ns-cloud-e1.googledomains.com", 
                                                                "ns-cloud-e2.googledomains.com", 
                                                                "ns-cloud-e3.googledomains.com",
                                                                "ns-cloud-e4.googledomains.com"],)
#    dns_settings = domains_v1.types.DnsSettings.GoogleDomainsDns() 
    print((dns_settings))
    print(type(dns_settings))

    # Initialize request argument(s)
    registration = domains_v1.Registration()
    registration.domain_name = requested_domain
    registration.contact_settings.privacy = "REDACTED_CONTACT_DATA"
    registration.contact_settings.registrant_contact.email = email
    registration.contact_settings.registrant_contact.phone_number = phone
    registration.contact_settings.admin_contact.email = email
    registration.contact_settings.admin_contact.phone_number = phone
    registration.contact_settings.technical_contact.email = email
    registration.contact_settings.technical_contact.phone_number = phone
    registration.dns_settings = dns_settings


    request = domains_v1.RegisterDomainRequest(
        parent= location,  #"parent_value",
        registration=registration,
        validate_only=True
    )

    # Make the request
    operation = client.register_domain(request=request,)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)


def get_registration(domain):
    # Create a client
    client = get_client()

    # Initialize request argument(s)
    request = domains_v1.GetRegistrationRequest(
        name= f"{location}/registrations/{domain}",     # projects/*/locations/*/registrations/*.
    )

    # Make the request
    response = client.get_registration(request=request)

    # Handle the response
    print(response)



def retrieve_register_parameters(domain):
    # Create a client
    client = get_client()

    # Initialize request argument(s)
    request = domains_v1.RetrieveRegisterParametersRequest(
        domain_name = domain,
        location = location,
    )

    # Make the request
    response = client.retrieve_register_parameters(request=request)

    # Handle the response
    print(response)



#domain = "kellerhome.dev"
domain = "kellerhome.io"

#print(check_available(domain))

#print(is_available(domain))

#print(search_domains(domain))

print(register_domain(domain))

#get_registration(domain)

#retrieve_register_parameters(domain)

