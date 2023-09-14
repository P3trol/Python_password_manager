from hashlib import pbkdf2_hmac
from unittest import result 

import utils.aesutil
import pyperclip

from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes

from matplotlib.pyplot import table
from utils.dbconfig import dbconfig1

from rich import print as printc
from rich.console import Console
from rich.table import Table



def computeMasterKey(mp, ds):
     password = mp.encode()
     salt = ds.encode()
     key = key = pbkdf2_hmac("sha512", password, salt, 100000, 32)
     return key



def retriveEntries(mp,ds,search ,decryptPassword = False):
    db = dbconfig1()
    cursor = db.cursor()
    
    query = "" 
    

    
    if len(search) == 0:
        query = "SELECT * FROM pm.entries"
    else:
        query ="SELECT * FROM pm.entries WHERE "
        for i in search:
                query+=f"{i} = '{search[i]}' AND "
        query = query[:-5]
        
    cursor.execute(query)
    result = cursor.fetchall()
    
    if len(result) == 0:
        printc("[yellow][-][/yellow] no results for this search")
        return
        
    if (decryptPassword and len(result)>1) or (not decryptPassword):
        table = Table(title= "Reults")
        table.add_column("Site Name")
        table.add_column("URL")
        table.add_column("Email")
        table.add_column("Username")
        table.add_column("Passowrd")
        
        for i in result:
          table.add_row(i[0],i[1],i[2],i[3],"{hidden}")
        console = Console()
        console.print(table)
    
        return
    if len(result) ==1 and decryptPassword:
        mk = computeMasterKey(mp, ds)
        decrypted = utils.aesutil.decrypt(key= mk, source=result[0][4], keyType="bytes")
        
        printc("[green][+][/green] password copied to clipboard")
        pyperclip.copy(decrypted.decode())
        
        
        
    db.close()
        
            
    
        
        
    
    
         
                 