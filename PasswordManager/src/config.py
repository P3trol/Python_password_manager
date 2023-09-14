from getpass import getpass
import hashlib
import random
import string
import sys
from utils.dbconfig import dbconfig1



from rich import print as printc
from rich.console import Console

def generateDeviceSecret(lenght=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = lenght))

def config():
    #creating the database
    db = dbconfig1()
    cursor = db.cursor()
    
    try:
        cursor.execute("CREATE DATABASE pm")
    except Exception as e:
        printc('[red] [!] an erroer ocurred while trying to create database.')
        Console.print_exception(show_locals=True)
        sys.exit(0)
    printc("[green][+][/green] Database 'pm' created") 
    
    #Create tables
    query = "CREATE TABLE pm.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"   
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'secrets' created ")
    
    query = "CREATE TABLE pm.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL)"   
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'entires' created ") 
    
    mp =""
    
    while (True):
        mp = getpass("choose a MASTER PASSWRD: ")
        if mp==getpass("re-type: ") and mp!="":
         break 
        printc("[yellow][-] please try again.[/yellow]")
        
    
    
        
    #hash the MASTER PASSWORD
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    printc("[green][+][/green] Generated hash of MASTER PASSWORD")
    
    #generate device sercret
    ds = generateDeviceSecret()
    printc("[green][+][/green] Generated Device Secret")
    
    #adding them to db
    query = "INSERT INTO pm.secrets (masterkey_hash, device_secret) values (%s, %s)"
    val = (hashed_mp, ds)
    res = cursor.execute(query, val)
    db.commit()
    
    printc("[green][+][/green] Added to the database")
    
    printc("[green][+] Configuration done [/green}")
    
    db.close()
    
    
    
config()
    
    
    
    
    
        
