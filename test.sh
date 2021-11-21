#!/bin/sh
sudo mysql < kyuutils_test.sql
python3 setup.py test
