from flask import abort, session, redirect, url_for, json
from app import app, api, github
from flask.ext.restful import Resource, reqparse
import re
import base64

def responseResult(result):
    return {
        'msg'   : 'succeed',
        'result': result
    }

@github.access_token_getter
def token_getter():
    if session.get('github_access_token', None) is not None :
        return session.get('github_access_token', None)

class Login(Resource):
    def get(self):
        return github.authorize(scope = 'user,public_repo')

class CallBack(Resource):
    @github.authorized_handler
    def get(oauth_token, self):
        if oauth_token is None:
            return redirect(url_for('github-login'))
        session['github_access_token'] = oauth_token
        return responseResult({
                'login': 'login succeed !'
            }), 201

class GetUser(Resource):
    def get(self):
        response = github.get('user')
        return responseResult({
                'account': {
                    'user' : response['login'],
                    'id'   : response['id'],
                    'name' : response['name'],
                    'pic'  : 'https://avatars3.githubusercontent.com/u/' + str(response['id']) + '?v=3&s=100',
                    'email': response['email']
                }
            }), 201

class Repos(Resource):
    def get(self, user):
        response =  github.get('users/' + user + '/repos')
        repos = []
        for repo in response:
            repos.append(
                {
                    'name'   : repo['name'],
                    'private': repo['private']
                }
            )
        return responseResult({
                'repos': repos
            }), 201

class Branchs(Resource):
    def get(self, user, repo):
        response = github.get('repos/' + user + '/' + repo + '/branches')
        branchs = []
        for branch in response:
            branchs.append(
                {
                    'name': branch['name'],
                    'sha' : branch['commit']['sha']
                }
            );

        return responseResult({
                'branchs': branchs
            }), 201

class TreeFile(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('fe', type = str)

    def get(self, user, repo, sha):
        args = self.reqparse.parse_args()
        fe = args.fe
        response = github.get('repos/' + user + '/' + repo + '/git/trees/' + sha + '?recursive=1' )
        files = []
        for tree in response['tree']:
            match = re.search(fe, tree['path'])
            if match is not None:
                files.append(
                    {
                        'url' : tree['url'],
                        'path': tree['path']
                    }
                )

        return responseResult({
                'files': files
            }), 201

class File(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type = str)

    def get(self):
        args = self.reqparse.parse_args()
        response = github.get(args.url)
        content = base64.b64decode(response['content'])
        return responseResult({
                'content': content
            }), 201

api.add_resource(Login, '/github/login', endpoint = 'github-login')
api.add_resource(CallBack, '/github/callback', endpoint = 'github-callback')
api.add_resource(GetUser, '/github/user', endpoint = 'github-user')
api.add_resource(Repos, '/github/repos/<user>', endpoint = 'github-repos')
api.add_resource(Branchs, '/github/branchs/<user>/<repo>', endpoint = 'github-branch')
api.add_resource(TreeFile, '/github/tree_file/<user>/<repo>/<sha>', endpoint = 'github-tree-file')
api.add_resource(File, '/github/file', endpoint = 'github-file')