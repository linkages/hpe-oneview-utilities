# hpe-oneview-utilities
A repository with a bunch of tools used to manage HPE infrastructure

This is where I keep a bunch of utilities that I use to manage an HPE Synergy environment.

# Getting started
These tools use a bunch of python libraries.
I prefer to manage usage of those libraries by using a python virtual environment.
To do that I do the following to create a virtualenv:

```
virtualenv hpeOneView
source hpeOneView/bin/activate
```

While the virtualenv is active, install the requirements by doing the following:

```
pip install -r ./requirements.txt
```

You will now have all the python requirements needed to run the tools in this repo.

# oneview-iLO
Some tools to configure things on the iLO of Synergy blades.
Right now it just gets users from each blade or create a new user on each blade.
