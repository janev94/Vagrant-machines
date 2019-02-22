#!/bin/bash
echo 'Resolving dependencies'
apt-get install git -y
mkdir setup
cd setup
wget https://dl.google.com/go/go1.11.5.linux-amd64.tar.gz
echo 'Setting up Go'
tar -C /usr/local -xzf go1.11.5.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
export GOPATH=`go env GOPATH`
export GOROOT=`go env GOROOT`

echo 'Resolving grabber deps'
### Get the original quic-go
go get github.com/lucas-clemente/quic-go
cd $GOPATH/src/github.com/lucas-clemente/quic-go

### Get the our modifications in quic-go
git remote add Eichhoernchen https://github.com/Eichhoernchen/quic-go.git
git fetch Eichhoernchen
git checkout -b qtracer Eichhoernchen/qtracer
cd $GOPATH/src/github.com
echo 'Done resolving grabber deps'