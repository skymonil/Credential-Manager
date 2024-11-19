from dbconfig import dbconfig
from getpass import  getpass
from rich import print as printc
from rich import console as Console
from rich.table import Table
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
import pyperclip
from Crypto.Random import get_random_bytes
import aes256
def computeMasterKey(master,devSec):
   password=master.encode()
   salt=devSec.encode()
   key=PBKDF2(password,salt,32,count=1000000,hmac_hash_module=SHA512)
   return key
def retrieveEntries(master,devSec,search,decryptPass=False):
    db=dbconfig()
    cursor=db.cursor()
    query=""
    db.database="Credentials"
    if len(search)==0:
        query="SELECT * FROM pass_vault"
    else:
        query="Select * from pass_vault where"
        for i in search:
            query+=f"{i} = '{search[i]}' AND "
        query=query[:-5]
    cursor.execute(query)
    results=cursor.fetchall() # fetching all results and storing them in a list
    if len(results)==0:
        printc("[RED][-] No Results found for the given search") 
        return
    
    if(decryptPass and len(results)>1) or(not decryptPass):
        table=Table(title="Results")
        table.add_column("Site Name")
        table.add_column("URL")
        table.add_column("Email")
        table.add_column("Username")
        table.add_column("Password")
        
        for i in results:
            table.add_row(i[0],i[1],i[2],i[3], "{hidden}")
            
            console=Console()
            console.print(table)
            return
        if len(results==1) and decryptPass:
            mk=computeMasterKey(master,devSec)
            decrypted=aes256.decrypt(key=mk,source=results[0][4],keyType="bytes")
            
            #copying the pass to the clipboard
            pyperclip.copy(decrypted.decode())
            printc("[green][+] Password copied to the clipboard")
