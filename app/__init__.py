from flask import Flask
from flask.ext import restful
from flask.ext.restful import fields
from flask.ext.github import GitHub
from flask import make_response
from bson.json_util import dumps

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = 'XXX'
app.config['GITHUB_CLIENT_SECRET'] = 'YYY'

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp


DEFAULT_REPRESENTATIONS = {'application/json': output_json}

api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS



#from app import books, book, search, users, login, logout
