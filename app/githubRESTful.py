from flask import abort
from app import app, api, github
from flask.ext.restful import Resource

class GithubLogin(Resource):
	def get(self):
		return github.authorize()

class GithubCallBack(Resource):
	@github.authorized_handler
	def get(self, oauth_token):
		github_access_token = oauth_token
		print 'github_access_token >>', github_access_token

api.add_resource(GithubLogin, '/github-login', endpoint = 'github-login')
api.add_resource(GithubCallBack, '/github-callback', endpoint = 'github-callback')