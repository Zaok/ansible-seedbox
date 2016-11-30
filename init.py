#!/usr/bin/python

import os, crypt, getpass
from pwd import getpwnam

def createUser(username, password):
    cryptPwd = crypt.crypt(password, "xD")
    return os.system("useradd -p "+cryptPwd+ " -s "+ "/bin/bash"+ " -d " +"/home/" + username+ " -m "+ " " + username)

#Create user account
username=raw_input("Username ?\n")
password=getpass.getpass("Password ?\n")
createUser(username, password)

#Get last digit of uid to create personal rep
uid=getpwnam(username).pw_uid
uid=str(uid)[3]

#Create Apache/rtorrent mount
os.system("""cat << EOT >> /etc/apache2/apache2.conf
#User: %s
"SGIMount /RPC%s 127.0.0.1:30%s00"
EOT""" % (username, username.upper(), uid))

os.system("service apache2 restart")
