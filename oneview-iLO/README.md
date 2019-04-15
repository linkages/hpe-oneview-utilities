# oneview-iLO utilities
Tools used to create and get all iLO users across all blades in a Synergy pod

## Setup
Before you use these tools you need to setup config.json.
An example file is located in config.json.example

It looks like this:

```
{
    "ip": "your-hostname-here.com",
    "api_version": "600",
    "credentials": {
        "userName": "Administrator",
        "password": "Password"
    }
}
```

replace:

your-hostname-here.com with the OneView management IP address of hostname
userName and password with the appropriate credentials

## getIloUsers.py
This will show you the iLO users defined on every blade in the Synergy domain

## createIloUser.py
This will create a new iLO user on every blade in the Synergy domain. 
You will need to modify this script to set the username and password.

Edit the following lines in the script:

```
ilo_username = "USERNAME"
ilo_password = "PASSWORD"
ilo_description = "User used by Amplifier pack to get stats to InfoSight"
ilo_name = "Amplifier Pack User"
```
