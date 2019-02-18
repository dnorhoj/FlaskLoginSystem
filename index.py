from flask import Flask, render_template, request, session, redirect
import auth, json

# Set up app
app = Flask(__name__)
app.secret_key = json.load(open("data.json"))["secret"]
PORT = 5000

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
		if code == 0:
			return "User created!<br><a href='/login'>Click here to go back</a>"
		elif code == 1:
			return render_template("register.html", criteria=True)
		elif code == 2:
			return "Username already in database."
		elif code == 3:
			return "Email already in database."
		else:
			return "Unknown Error"

	return render_template("register.html", criteria=False)

@app.route('/me')
def me():
	return session.get('username', 'Not logged in')

if __name__ == '__main__':
	app.run(
		debug=True, host='0.0.0.0',
		port=PORT,
		#ssl_context='adhoc'
	)