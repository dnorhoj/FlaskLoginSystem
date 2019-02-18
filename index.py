from flask import Flask, render_template, request, session, redirect
import auth

# Set up app
app = Flask(__name__)
PORT = 8000

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def loginsite():
	if request.method == 'POST':
		form = request.form.get
		
		if auth.login(form('uname'), form('pass')):
			return "True :)"
		return "False :("

	return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def registersite():
	return render_template("register.html")

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=PORT)