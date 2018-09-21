from flask import Flask, request, make_response, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    username = request.cookies.get('username')
    print(username)
    resp = make_response()
    resp.set_cookie('username', 'han')
    return resp
