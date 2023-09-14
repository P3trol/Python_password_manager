from threading import local
import mysql.connector 

from rich import print as printc
from rich.console import Console
console = Console() 

def dbconfig1():
 try:
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'pm',
        passwd = 'password'
    )
 except Exception as e:
     console.print_exception(show_locals=True)
     
 return db

     

