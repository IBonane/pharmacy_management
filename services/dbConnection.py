from mysql.connector import Error
import sys


def dbconnection(mysql_connector, params_connection):
    try:
         
        print("connection à la base de donnée en cours")

        connection = mysql_connector.connect(**params_connection)

        if connection.is_connected():
            print("connection à la base de donnée réussie")
            return connection
    
    except Error as e:
    
        print("""\nConnection à la base de donnée 'pharmacie' non établie.
              veuillez vérifier votre fichier config.py et vous assurer que mysql est bien démarré
              ou que la base de donnée 'pharmacie' exist."""
        )
        sys.exit(0)

