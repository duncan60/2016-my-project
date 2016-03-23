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
                'user': response['login']
            }), 201

class Repos(Resource):
    def get(self, login):
        response =  github.get('users/' + login + '/repos')
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
    def get(self, user, repo, sha):
        response = github.get('repos/' + user + '/' + repo + '/git/trees/' + sha + '?recursive=1' )
        files = []
        for tree in response['tree']:
            pat='.md'
            match = re.search(pat, tree['path'])
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
        self.reqparse.add_argument('path', type = str)

    def get(self):
        args = self.reqparse.parse_args()
        response = github.get(args.path)
        content = base64.b64decode(response['content'])
        return responseResult({
                'content': content
            }), 201

api.add_resource(Login, '/github/login', endpoint = 'github-login')
api.add_resource(CallBack, '/github/callback', endpoint = 'github-callback')
api.add_resource(GetUser, '/github/user', endpoint = 'github-user')
api.add_resource(Repos, '/github/repos/<login>', endpoint = 'github-repos')
api.add_resource(Branchs, '/github/branchs/<user>/<repo>', endpoint = 'github-branch')
api.add_resource(TreeFile, '/github/tree_file/<user>/<repo>/<sha>', endpoint = 'github-tree-file')
api.add_resource(File, '/github/file', endpoint = 'github-file')