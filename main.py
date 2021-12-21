import hmac, base64, struct, hashlib, time, json, os
from flask import Flask, render_template, jsonify, request


def get_hotp_token(secret, intervals_no):
	"""This is where the magic happens."""
	key = base64.b32decode(normalize(secret), True) # True is to fold lower into uppercase
	msg = struct.pack(">Q", intervals_no)
	h = bytearray(hmac.new(key, msg, hashlib.sha1).digest())
	o = h[19] & 15
	h = str((struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000)
	return prefix0(h)


def get_totp_token(secret):
	"""The TOTP token is just a HOTP token seeded with every 30 seconds."""
	intervals_no = int(time.time()) // 30

	return get_hotp_token(secret, intervals_no), int(time.time())


def normalize(key):
	"""Normalizes secret by removing spaces and padding with = to a multiple of 8"""
	k2 = key.strip().replace(' ','')
	# k2 = k2.upper()	# skipped b/c b32decode has a foldcase argument
	if len(k2)%8 != 0:
		k2 += '='*(8-len(k2)%8)
	return k2


def prefix0(h):
	"""Prefixes code with leading zeros if missing."""
	if len(h) < 6:
		h = '0'*(6-len(h)) + h
	return h


def main():
	kp = {}
	rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	with open(os.path.join(rel,'secrets.json'), 'r') as f:
		secrets = json.load(f)
	for label, key in sorted(list(secrets.items())):
		#kp.append(dict({label : get_totp_token(key)}))
		code, time_1= get_totp_token(key)
		kp[label] = {'code': code, 'time':time_1}
		print("{}:\t{}".format(label, get_totp_token(key)))
	print(kp)
	return kp


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	all_kps = main()
	if request.args.get('api') == "true":
		return jsonify(all_kps)

	return render_template('base.html',kps= all_kps)

if __name__ == "__main__":
	app.run(debug=True)

