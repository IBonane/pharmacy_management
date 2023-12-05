from mysql.connector import Error


def dbconnection(mysql_connector, params_connection):
    try:
         
        print("connection à la base de donnée en cours")

        connection = mysql_connector.connect(**params_connection)

        if connection.is_connected():
            print("connection à la base de donnée réussie")
            return connection
    
    except Error as e:
    
        print("La connection a échoué")
        return None

