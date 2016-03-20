from flask import abort, g, session, redirect, url_for, json
from app import app, api, github
from flask.ext.restful import Resource

github_access_token = None

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

		github_access_token = oauth_token
		session['github_access_token'] = github_access_token
		return {
			'oauth_token': github_access_token
		}

class GetUser(Resource):
	def get(self):
		return github.get('user')

class Repos(Resource):
	def get(self, login):
		return github.get('users/' + login + '/repos')

api.add_resource(Login, '/github/login', endpoint = 'github-login')
api.add_resource(CallBack, '/github/callback', endpoint = 'github-callback')
api.add_resource(GetUser, '/github/user', endpoint = 'github-user')
api.add_resource(Repos, '/github/repos/<login>', endpoint = 'github-repos')