#!/bin/bash

echo 'Copying files'

cp /home/vagrant/src/probe_servers.py /root/go/src/github.com/Eichhoernchen/quic-grabber/probe_servers.py
cp /home/vagrant/src/extract_versions.py /root/go/src/github.com/Eichhoernchen/quic-grabber/extract_versions.py


cd /root/go/src/github.com/Eichhoernchen/quic-grabber/
wget https://gist.githubusercontent.com/janev94/29e9b8c9d20d463be0c43376583626e1/raw/78f6dbf2fabbf30d958b935a5f13c471befca1dd/servers_feb

cp /home/vagrant/src/Makefile ./Makefile

# make result folder
mkdir res
# make errors folder
mkdir errors

echo 'Done'
