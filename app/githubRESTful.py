from flask import abort, session, redirect, url_for, json
from app import app, api, github
from flask.ext.restful import Resource, reqparse
import base64

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
		return {
			'msg': 'login successed !'
		}

class GetUser(Resource):
	def get(self):
		response = github.get('user')
		return {
			'msg'   : 'successed',
			'result': {
				'login': response['login']
			}
		}, 201

class Repos(Resource):
	def get(self, login):
		return github.get('users/' + login + '/repos')

class Branchs(Resource):
	def get(self, user, repo):
		return github.get('repos/' + user + '/' + repo + '/branches')

class TreeFile(Resource):
	def get(self, user, repo, sha):
		return github.get('repos/' + user + '/' + repo + '/git/trees/' + sha + '?recursive=1' )

class File(Resource):
	def __init__(self):
	    self.reqparse = reqparse.RequestParser()
	    self.reqparse.add_argument('path', type = str)

	def get(self):
		args = self.reqparse.parse_args()
		response = github.get(args.path)
		content = base64.b64decode(response['content'])
		return {
			'content': content
		}

api.add_resource(Login, '/github/login', endpoint = 'github-login')
api.add_resource(CallBack, '/github/callback', endpoint = 'github-callback')
api.add_resource(GetUser, '/github/user', endpoint = 'github-user')
api.add_resource(Repos, '/github/repos/<login>', endpoint = 'github-repos')
api.add_resource(Branchs, '/github/branchs/<user>/<repo>', endpoint = 'github-branch')
api.add_resource(TreeFile, '/github/tree_file/<user>/<repo>/<sha>', endpoint = 'github-tree-file')
api.add_resource(File, '/github/file', endpoint = 'github-file')