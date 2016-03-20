from flask import Flask
from flask.ext import restful
from flask.ext.restful import fields
from flask.ext.github import GitHub
from flask import make_response
import json
from config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = GITHUB_CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = GITHUB_CLIENT_SECRET

def output_json(obj, code, headers=None):
    resp = make_response(json.dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp


DEFAULT_REPRESENTATIONS = {'application/json': output_json}

api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS
github = GitHub(app)

from app import githubRESTful