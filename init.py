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

#Get last digit of uid to create personal id
uid=getpwnam(username).pw_uid
uid=str(uid)[3]

#Create Apache/rtorrent mount for the user
os.system("""cat << EOT >> /etc/apache2/apache2.conf
#User: %s
"SGIMount /RPC%s 127.0.0.1:30%s00"
EOT""" % (username, username.upper(), uid))

os.system("service apache2 restart")

#Create needed folders for the new user
os.system("sudo -u %s mkdir -p /home/%s/{torrents,watch,.session}" % (username,username))

#Configure rtorrent
os.system("""cat << EOT >> /home/%s/.rtorrent.rc
scgi_port = 127.0.0.1:30%s00
encoding_list = UTF-8
port_range = 45000-65000
port_random = no
check_hash = no
directory = /home/%s/torrents
session = /home/%s/.session
encryption = allow_incoming, try_outgoing, enable_retry
schedule = watch_directory,1,1,"load_start=/home/%s/watch/*.torrent"
schedule = untied_directory,5,5,"stop_untied=/home/%s/watch/*.torrent"
use_udp_trackers = yes
dht = off
peer_exchange = no
min_peers = 40
max_peers = 100
min_peers_seed = 10
max_peers_seed = 50
max_uploads = 15
execute = {sh,-c,/usr/bin/php /var/www/html/rutorrent/php/initplugins.php %s &}
schedule = disk_space_error,1,30,close_low_diskspace=500M
EOT""" % (username,uid,username,username,username,username,username))

#Create rutorrent folder for the user
os.system("sudo -u www-data mkdir /var/www/html/rutorrent/conf/users/%s" % (username))
os.system("""cat << EOT >> /var/www/html/rutorrent/conf/users/%s/config.php
<?php

$pathToExternals['curl'] = '/usr/bin/curl';
$topDirectory = '/home/%s';
$scgi_port = 30%s00;
$scgi_host = '127.0.0.1';
$XMLRPCMountPoint = '/RPC%s';
EOT""" % (username,username,uid,username.upper()))

os.system("chown www-data:www-data /var/www/html/rutorrent/conf/users/%s/config.php" % (username))
print("Password for %s rutorrent\n" % (username))
if os.path.exists(/etc/apache2/auth/webauth):
    os.system("htdigest /etc/apache2/auth/webauth webserver %s" % (username))
else:
    os.system("htdigest -c /etc/apache2/auth/webauth webserver %s" % (username))

os.system("service apache2 restart")
