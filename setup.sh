#!/bin/sh

#prerequisites
yum -y groupinstall "Development Tools"
yum install git -y
wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
sudo -H python get-pip.py
yum install gtk2-devel gtk+-devel bison qt-devel qt5-qtbase-devel -y
yum install python-pip -y
yum install python-devel -y
yum install gcc gcc-devel -y
yum install libxml2 libxml2-devel -y
yum install libxslt libxslt-devel -y
yum install openssl openssl-devel -y
yum install libffi libffi-devel -y
yum install libpcap-devel -y
yum install screen -y


#python dependencies
sudo python python_dependency.py install

#adduser
sudo python adduser.py
