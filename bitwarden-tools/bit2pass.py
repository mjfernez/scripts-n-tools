#!/usr/bin/python3
"""
bit2pass.py - grabs the bare minimum info from a bitwarden JSON export
(unencrypted) to populate a UNIX pass datastore. This assumes you named
your entry and gave it a password, otherwise, this script will yell at
you.

This does NOT grab notes or usernames. I use pass purely for easy (and
secure) copying of passwords. If I really need the notes, it's probably
not something I'm going to be copying much. I also exclude anything
that's not a login because, well that's what bitwarden's good for...
Don't limit yourself to one tool


Usage:
0) (before running) Initialize a pass database:
    pass init
1) python bit2pass.py <your-file>
"""
import sys
import subprocess
import json
with open(sys.argv[1]) as f:
    data = json.load(f)

folders = { x['id'] : x['name'] for x in data['folders'] }
passwords = {
            folders[x['folderId']] + '/' + x['name'] :
            x['login']['password']
            for x in data['items']
            if x['type'] == 1
    }
print(passwords)

for p in passwords:
    echo = subprocess.run(["echo", passwords[p]],
            check=True,
            capture_output=True
    )
    pass2pass = subprocess.run(["pass", "insert", "-e", p],
            input=echo.stdout,
            capture_output=True
    )
    print(pass2pass.stdout)
