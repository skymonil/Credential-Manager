from getpass import getpass
from dbconfig import dbconfig
from rich import print as printc
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import aes256
def computeMasterKey(master,devSec):
   password=master.encode()
   salt=devSec.encode()
   key=PBKDF2(password,salt,32,count=1000000,hmac_hash_module=SHA512)
   return key
    
def addEntry(master,devSec,sitename,siteurl,email,username):
    #getting the password
    password=getpass("Password:")
    
    mk=computeMasterKey(master,devSec)
    
    encrypted= aes256.encrypt(key=mk,source=password,keyType="bytes")
    
    #Adding to DB
    db=dbconfig()
    db.database="Credentials"
    cursor=db.cursor()
    query="INSERT INTO pass_vault (sitename, siteurl,email,username,password) VALUES (%s, %s,%s,%s,%s)"
    cursor.execute(query,(sitename,siteurl,email,username,encrypted))
    db.commit()
    printc("[green][+] Entry Added Successfully")
    