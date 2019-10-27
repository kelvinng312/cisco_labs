#!/usr/bin/env python
import sys

import requests
import json
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


# Enter all authentication info
SMC_USER = "admin"
SMC_PASSWORD = "WWTwwt1!"
SMC_HOST = "192.168.128.109"

def post(api_session, url, payload):

    request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = api_session.request("POST", url, verify=False, data=json.dumps(payload), headers=request_headers)

    json_data = json.loads(response.text)

    status = response.status_code
    content = response.text

    print('query url=' + url)
    print('  response=' + content)

    return status, content

def getTenantId(api_session):
    # Get the list of tenants (domains) from the SMC
    url = 'https://' + SMC_HOST + '/sw-reporting/v1/tenants/'
    response = api_session.request("GET", url, verify=False)
    print('query url=' + url)
    print('  response=' + str(response))

    # If successfully able to get list of tenants (domains)
    if (response.status_code == 200):
        # Store the tenant (domain) ID as a variable to use later
        tenant_list = json.loads(response.content)["data"]
        tenant_id = tenant_list[0]["id"]

        return tenant_id
    return None

if __name__ == '__main__':

    # Initialize the Requests session
    api_session = requests.Session()

    # Login
    url = "https://" + SMC_HOST + "/token/v2/authenticate"
    login_request_data = {
        "username": SMC_USER,
        "password": SMC_PASSWORD
    }
    status, content = post(api_session, url, login_request_data)

    if status != 200:
        print("An error has ocurred, while logging in, with the following code {}".format(status))
        exit(0)

    # Print the menu
    print("""
                 Stealth Watch Management
              ACME Inc, IT Security Department

                Top Alarming Hosts:    
    """)

    # Get tenant Id
    tenant_id = getTenantId(api_session)
    if tenant_id is None:
        print("Can not get a tenant Id.")
        exit(0)

    # Get the list of tenants (domains) from the SMC
    url = 'https://' + SMC_HOST + '/sw-reporting/v1/tenants/' + str(tenant_id) + "/internalHosts/alarms/topHosts"
    response = api_session.request("GET", url, verify=False)

    # If failed
    if (response.status_code != 200):
        print("Get top alarming hosts failed.")
        exit(0)

    results = json.loads(response.content)

    # Filter out the valid items and print it
    for item in results:
        print(item)


