from dbconfig import dbconfig
from rich import print as printc
from rich.console import Console
import mysql.connector
import hashlib
import random
import sys
import string
import getpass
console=Console()

def genDevSec(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k= length))
def config():
     # Creating a database
     db=dbconfig()
     cursor=db.cursor()
     try:
         cursor.execute("Create database IF NOT EXISTS Credentials")
     except Exception as e:
         printc("[red][!] Failed to Create Database")
         console.print_exception(show_locals=True)
         sys.exit(0)
     db.database="Credentials"
     
     #Creating Tables
     query="Create Table IF NOT EXISTS secrets(master_hash varchar(255) NOT NULL,device_sec varchar(255) NOT NULL)"
     cursor.execute(query)
     printc("[green][+] Table secrets created")
     
     query= "Create Table IF NOT EXISTS  pass_vault(sitename varchar(255) NOT NULL, siteurl varchar(255) NOT NULL,email varchar(40),username varchar(50), password varchar(255) NOT NULL)"
     cursor.execute(query)
     printc("[green] [+] Table Containing Passwords created")
     
     while 1:
         master=getpass.getpass("choose a master PASSWORD: ")
         if master==getpass.getpass("Confirm Your Passoword ") and master!="":
             break
         printc("[red][!] Both passwords do not match")
     
     #hashing the masterpass
     hashed_master=hashlib.sha256(master.encode()).hexdigest()
     printc("[green][+]Generated hash of master password")
     
     #Generating a device secret
     devSec=genDevSec()
     printc("[green][+]Generated hash of Master Password")
     
     # Add them to db
     query = "INSERT INTO secrets (master_hash, device_sec) VALUES (%s, %s)"
     cursor.execute(query,(hashed_master,devSec))
     db.commit()
     
     printc("[green][+] Configuration Done")
     db.close()
     
        
    
    
    
     
     

    
config()