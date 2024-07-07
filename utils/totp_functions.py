import hmac, base64, struct, hashlib, time, json, os
import json

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
	currtime = int(time.time())
	intervals_no = currtime // 30
	next_refresh_time = intervals_no * 30 + 30
	print(f"currtime = {currtime} intervals no = {intervals_no}")
	return get_hotp_token(secret, intervals_no), next_refresh_time	


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

def create_2fa_kps(secrets_path):
	kp = {}
#	rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	with open(secrets_path, 'r') as f:
		secrets = json.load(f)
	for label, key in sorted(list(secrets.items())):
		#kp.append(dict({label : get_totp_token(key)}))
		code, time_1= get_totp_token(key)
		kp[label] = {'code': code, 'expiry': time_1}
		print("{}:\t{}".format(label, get_totp_token(key)))
	print(kp)
	return kp

def save_new_secret(secrets_path, secret_key, label):
    data = {}
    try:
        with open(secrets_path, 'r') as file:
            data = json.load(file)
        with open(secrets_path, 'w') as f:
            try:
                data[label] = text_to_base32(secret_key)
                f.write(json.dumps(data))
            except BaseException as e:
                print("could not write to file")
                return -1
    except BaseException as e:
        print("could not write to file 2")
        print(f"{e}")


def text_to_base32(text):
    # Convert text to bytes
    text_bytes = text.encode('utf-8')
    
    # Encode bytes to Base32
    base32_bytes = base64.b32encode(text_bytes)
    
    # Convert bytes back to a UTF-8 string
    base32_text = base32_bytes.decode('utf-8')
    
    return base32_text