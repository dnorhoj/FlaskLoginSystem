import json, hashlib

# Filenames
DATA = "data.json"

def login(username, password):
	with open("data.json") as f:
		data = json.loads(f.read())
		if not username in data["users"]:
			return False
		
		saltedpass = password+data["salt"]
		encryptedpass = hashlib.sha256(saltedpass.encode()).hexdigest()

		print(saltedpass)
		print(encryptedpass)

		if data["users"][username]["password"] == encryptedpass:
			return True
		
		print("OOF")
		return False