
from getpass import getpass
from hashlib import pbkdf2_hmac
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64
import sys

from utils.dbconfig import dbconfig1
import utils.aesutil
from utils.aesutil import encrypt

from rich import print as printc
from rich.console import Console



def computeMasterKey(mp, ds):
     password = mp.encode()
     salt = ds.encode()
     #key = PBKDF2(password, salt, 32, count = 1000000, hmac_hash_module=SHA512)
     key = pbkdf2_hmac("sha512", password, salt, 100000, 32)
     return key


def checkEntry(sitename, siteurl, email, username):
	db = dbconfig1()
	cursor = db.cursor()
	query = f"SELECT * FROM pm.entries WHERE sitename = '{sitename}' AND siteurl = '{siteurl}' AND email = '{email}' AND username = '{username}'"
	cursor.execute(query)
	results = cursor.fetchall()

	if len(results)!=0:
		return True
	return False




def addEntry(mp, ds, sitename, siteurl, email, username):
	# Check if the entry already exists
	if checkEntry(sitename, siteurl, email, username):
		printc("[yellow][-][/yellow] Entry with these details already exists")
		return

	# Input Password
	password = getpass("Password: ")

	# compute master key
	mk = computeMasterKey(mp, ds)

	# encrypt password with mk
	encrypted = utils.aesutil.encrypt(key=mk, source=password, keyType="bytes")

	# Add to db
	db = dbconfig1()
	cursor = db.cursor()
	query = "INSERT INTO pm.entries (sitename, siteurl, email, username, password) values (%s, %s, %s, %s, %s)"
	val = (sitename,siteurl,email,username,encrypted)
	cursor.execute(query, val)
	db.commit()

	printc("[green][+][/green] Added entry ")
