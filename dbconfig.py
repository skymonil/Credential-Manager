from rich.console import Console
console=Console()
import mysql.connector
def dbconfig():
    try:
        db=mysql.connector.connect(
            host="localhost",username="root",password="root@765"
        )
    except Exception as e:
        console.print_exception(show_locals=True)
    return db