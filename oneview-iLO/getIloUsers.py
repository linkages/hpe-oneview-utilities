#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pprint import pprint
from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient
import re
from RedfishObject import RedfishObject
import logging

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--host", help="OneView host. If not specified uses default from config.json", default="none")
args = parser.parse_args()

# Try load config from a file (if there is a config file)
config = try_load_from_file(file_name="./config.json")

if args.host != "none":
    config['ip'] = args.host

oneview_client = OneViewClient(config)
server_hardwares = oneview_client.server_hardware

# Get list of all server hardware resources
print("Get list of all server hardware resources")
#server_hardware_all = server_hardwares.get_ilo_sso_url("/rest/server-hardware/33323337-3035-5355-4537-323843594B44")
server_hardware_all = server_hardwares.get_all()

for server in server_hardware_all:
    remote_console_url = server_hardwares.get_remote_console_url(server['uri'])

    print("Name:\t{name}\nRemote:\t{remote}".format(name=server['name'],remote=remote_console_url))
    # This will get the remote address of the iLO interface
    ssoRootUriHostAddressMatchObj = re.search( r'addr=(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})', remote_console_url['remoteConsoleUrl'], re.M|re.I)

    # This will get the session token that you will then use to pass to the iLO RedFish interface
    ssoTokenMatchObj = re.search( r'sessionkey=(\S*)$', remote_console_url['remoteConsoleUrl'], re.M|re.I)  

    server_address = "https://" + ssoRootUriHostAddressMatchObj.group(1).strip()
    authToken = ssoTokenMatchObj.group(1).strip()

    redFishSsoSessionObject = { "RootUri": server_address, "Token": authToken }

    print("Addr:\t{address}\nToken:\t{token}\n".format(token=authToken, address=server_address))

    # Create a REDFISH object
    try:        
        redfishObj = RedfishObject(server_address, redFishSsoSessionObject['Token'], logging.DEBUG)
    except ServerDownOrUnreachableError as excp:
        sys.stderr.write("ERROR: server not reachable or doesn't support RedFish.\n")
        sys.exit()
    except Exception as excp:
        raise excp

    instances = redfishObj.search_for_type("AccountService.")
    print("Instances: ")
    pprint(instances)
    print("")

    for instance in instances:
        rsp = redfishObj.redfish_get(instance["@odata.id"])
        accounts = redfishObj.redfish_get(rsp.dict["Accounts"]["@odata.id"])
        print("Users: ")
        for entry in accounts.dict["Members"]:
            account = redfishObj.redfish_get(entry["@odata.id"])
            pprint(account.dict)
        print("")
