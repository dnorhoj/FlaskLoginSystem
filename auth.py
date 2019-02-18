import json, hashlib, re

# Filenames
DATAFILE = "data.json"

def login(username, password):
	with open(DATAFILE) as f:
		data = json.load(f)
		users = data["users"]
		user = {}

		for info in users.values():
			if info["username"] == username:
				user = info
		
		if user == {}:
			print(f"Username: {username} not found")
			return False
		
		saltedpass = password+data["salt"]
		encryptedpass = hashlib.sha256(saltedpass.encode()).hexdigest()

		if user["password"] == encryptedpass:
			return True
		
		return False
	
def register(username, password, email=None):
	"""
	Rules for password
	1. 7 tegn
	2. Mindst et stort bogstav
	3. Mindst et småt bogstav
	4. Mindst et tal
	"""
	with open(DATAFILE) as f:
		data = json.load(f)
		
		for user in data["users"].values():
			if user["username"] == username:
				return 2 # 2 = Username already exist
			elif user["email"] == email:
				return 3 # 3 = Email already exist

		if not checkpass(password):
			return 1 # 1 = Password does not meet criterias

		id = data["nextuser"]

		data["users"][id] = {}
		data["users"][id]["email"] = email
		data["users"][id]["username"] = username

		saltedpass = password+data["salt"]
		encryptedpass = hashlib.sha256(saltedpass.encode()).hexdigest()
		data["users"][id]["password"] = encryptedpass

		data["nextuser"] = str(int(data["nextuser"])+1)

		with open(DATAFILE, 'w') as outfile:  
			json.dump(data, outfile, indent=4)
			return 0 # 0 = Success

def checkpass(password):
	if re.match(r'.{7}', password) is None:
		return False