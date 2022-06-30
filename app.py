from flask import Flask, jsonify, request
from flask.json import JSONEncoder
app = Flask(__name__)

app.users={}
app.id_count = 1

@app.route('/sign-up', methods=['POST'])
def sign_up():
	new_user = request.json
	new_user['id'] = app.id_count
	app.users[app.id_count] = new_user
	app.id_count = app.id_count + 1
	return jsonify(new_user)

app.tweets=[]

@app.route('/tweet', methods=['POST'])
def tweet():
	payload = request.json
	user_id = int(payload['id'])
	tweet = payload['tweet']
	
	if user_id not in app.users:
		return 'cannot access', 400
	if len(tweet) > 300:
		return 'over 300 letters', 400
	
	app.tweets.append({
		'user_id' : user_id,
		'tweet' :  tweet
	})
	return '', 200
class CustomJSONEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, set):
			return list(obj)
		return JSONEncoder.default(self, obj)
app.json_encoder = CustomJSONEncoder

@app.route('/follow', methods=['POST'])
def follow():
	payload = request.json
	user_id = int(payload['id'])
	user_id_to_follow = int(payload['follow'])
	
	if user_id not in app.users or user_id_to_follow not in app.users:
		return 'does not exist user', 400
	user = app.users[user_id]
	user.setdefault('follow', set()).add(user_id_to_follow)
	return jsonify(user)
@app.route('/unfollow' , methods=['POST'])
def unfollow():
	payload = request.json
	user_id = int(payload['id'])
	user_id_to_follow = int(payload['unfollow'])

	if user_id not in app.users or user_id_to_follow not in app.users:
		return 'does not exist users', 400
	user = app.users[user_id]
	user.setdefault('follow', set()).discard(user_id_to_follow)
	return jsonify(user)
