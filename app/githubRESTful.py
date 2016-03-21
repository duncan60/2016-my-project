from flask import abort, g, session, redirect, url_for, json
from app import app, api, github
from flask.ext.restful import Resource


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
		return github.get('user')

class Repos(Resource):
	def get(self, login):
		return github.get('users/' + login + '/repos')

class Branchs(Resource):
	def get(self, user, repo):
		return github.get('repos/' + user + '/' + repo + '/branches')

class TreeFile(Resource):
	def get(self, user, repo, branch):
		return github.get('repos/' + user + '/' + repo + '/branches/' + branch )

api.add_resource(Login, '/github/login', endpoint = 'github-login')
api.add_resource(CallBack, '/github/callback', endpoint = 'github-callback')
api.add_resource(GetUser, '/github/user', endpoint = 'github-user')
api.add_resource(Repos, '/github/repos/<login>', endpoint = 'github-repos')
api.add_resource(Branchs, '/github/branchs/<user>/<repo>', endpoint = 'github-branch')
api.add_resource(TreeFile, '/github/tree_file/<user>/<repo>/<branch>', endpoint = 'github-tree-file')
