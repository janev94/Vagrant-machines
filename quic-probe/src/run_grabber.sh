#!/bin/bash
#should really split that into two seperate files for setup and run

#Add paths again, since make runs commands in seperate shells
export PATH=$PATH:/usr/local/go/bin
export GOPATH=`go env GOPATH`
export GOROOT=`go env GOROOT`

echo 'Setting up grabber'
cd $GOPATH/src/github.com
### Get the current quic-grabber
mkdir Eichhoernchen
cd $GOPATH/src/github.com/Eichhoernchen
git clone https://github.com/Eichhoernchen/quic-grabber
cd $GOPATH/src/github.com/Eichhoernchen/quic-grabber
go build
echo 'Done building grabber'
### At this point we have the go-grabber binary, so run that
### J.R. was kind enough to provide us with a working gQUIC server recently so use that to test

echo 'Running grabber'
pwd
echo '{"addr": "216.58.207.35:443", "sni": "www.google.de"}' | ./quic-grabber 
