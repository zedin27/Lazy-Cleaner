#!/bin/sh

if ! [ -e venv ]
then
	pip3 install virtualenv
	virtualenv -p python3 venv
	. venv/bin/activate
	pip3 install -r requirements.txt
else
	echo "installed"
	. venv/bin/activate
fi
