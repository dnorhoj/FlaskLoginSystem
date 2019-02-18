from flask import Flask, render_template, request, session, redirect
import auth, json

# Set up app
app = Flask(__name__)
app.secret_key = json.load(open("data.json"))["secret"]
PORT = 8000

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def loginsite():
	if request.method == 'POST':
		form = request.form.get
		
		if auth.login(form('uname'), form('pass')):
			session['username'] = form('uname')
			return redirect("/me")
		return "Wrong credentials :("

	return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def registersite():
	if request.method == 'POST':
		form = request.form.get
		
		code = auth.register(form('uname'), form('pass'), form('email'))
		login = (form('email'), form('uname'), form('pass'))
		if code == 0: # Success
			return "User created!<br><a href='/login'>Click here to go back</a>"
		elif code == 1: # Password does not pass criterias
			return render_template("register.html", criteria=True, login=login)
		elif code == 2: # Username exists
			return render_template("register.html", error="Username already exists.", login=login)
		elif code == 3: # Email exists
			return render_template("register.html", error="Email already exists.", login=login)
		elif code == 4: # No username entered
			return render_template("register.html", error="No username entered.", login=login)
		else:
			return "Unknown Error"

	return render_template("register.html")

@app.route('/me')
def me():
	return session.get('username', 'Not logged in')

if __name__ == '__main__':
	app.run(
		debug=True,
		host='0.0.0.0',
		port=PORT,
		#ssl_context='adhoc'
	)