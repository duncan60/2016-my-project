# flask-github-api
use flask connect github api 

## Installation
After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

```
$ virtualenv env
$ . env/bin/activate
(venv) $ pip install -r requirements.txt
```
## Start to development and running server
```
$ . env/bin/activate
(venv) $ python run.py
# open this url in your browser
# http://127.0.0.1:5000/
```

## RESTful-APIs
```
# github connect login
# get /github/login

# github loging succeed callback
# get /github/callback

# github user info
# get /github/user

# repositories list
# get /github/repos/<login>

# a repository has all branch
# get /github/branchs/<user>/<repo>

# a repository branch has all file info
# get /github/tree_file/<user>/<repo>/<sha>

# a .md file content
# get /github/file?path=<md path>
```
