# flask-github-api
use flask RESTful connect github api data

## Installation
After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

```
$ virtualenv env
$ . env/bin/activate
(venv) $ pip install -r requirements.txt
```
create github developer applications, setting authorization callback URL
```
http://127.0.0.1:5000/github/callback
```
create config.py, set value
```
GITHUB_CLIENT_ID = 'your applications ID'
GITHUB_CLIENT_SECRET = 'your applications secret'
```

## Start to development and running server
```
$ . env/bin/activate
(venv) $ python run.py
# open this url in your browser
# http://127.0.0.1:5000/
```

## RESTful-APIs

#### github authorizing users
```
# get /github/login
# response result:
account:{
    email: "your email",
    pic  : "your picture",
    user : "your account",
    name : "your name",
    id   : "your id"
}
```
#### github authorizing succeed callback
```
# get /github/callback
# response result:
{
    login: "login succeed !"
}
```
#### repositories list
```
# get /github/repos/<user>
# response result:
repos:[
    {
        name   : "repositorie name",
        private: false or name
    },
    ...more
]
```
#### a repository has all branch
```
# get /github/branchs/<user>/<repo>
# response result:
branchs:[
    {
        name: "branch name",
        sha : "commit sha"
    },
    ...more
]
```
#### a repository branch has all file info
```
# get /github/tree_file/<user>/<repo>/<sha>?fe=<filename extension>
# response result:
files:[
    {
        url : "file url",
        path: "file path"
    },
    ...more
]
```
#### a file content
```
# get /github/file?url=<file url>
# response result:
{
    content: "file content"
}
```
