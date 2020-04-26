tex2image
=========

Simple web service for sharing tex-based expression 

How to deploy
-------------
```sh
$ sudo apt install texlive-extra-utils dvipng
$ pip install requirements.txt -r
$ gunicorn tex2image:app
```
