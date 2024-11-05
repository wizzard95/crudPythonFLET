import sqlite3

# Creamos la clase para acceder a los diferentes métodos (CRUD)
class ContactManager:
    def __init__(self) -> None:  # Se inicializa el constructor
        # Se crea la variable/objeto de conexión
        self.connection = sqlite3.connect("data.db", check_same_thread=False)  

    # Método para agregar los datos  
    def add_contact(self, name, age, email, phone):
        query = ''' INSERT INTO datos(NOMBRE, EDAD, CORREO, TELEFONO)
                    VALUES (?, ?, ?, ?)
                '''
        # Ejecutamos la query que creamos recién            
        self.connection.execute(query, (name, age, email, phone))
        
        # Registramos los datos
        self.connection.commit()
            
    # Método para obtener los datos
    def get_contact(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM datos"  # Seleccionamos todos los elementos y los traemos desde la BD
        cursor.execute(query)
        
        # Retornamos los datos desde la BD
        contacts = cursor.fetchall()
        return contacts
        
    # Método para eliminar los datos
    def delete_contact(self, name):
        query = "DELETE FROM datos WHERE NOMBRE = ?"
        self.connection.execute(query, (name,))
        self.connection.commit()
        
    # Método para actualizar los datos de contacto
    def update_contact(self, contact_id, name, age, email, phone):
        query = '''UPDATE datos SET NOMBRE = ?, EDAD = ?, CORREO = ?, TELEFONO = ? WHERE ID = ?'''
        self.connection.execute(query, (name, age, email, phone, contact_id))
        self.connection.commit()
            
    # Método para cerrar la conexión
    def close_connection(self):
        self.connection.close()



# Ejemplo de uso con el archivo data.db
"""x = ContactManager()

print(x.get_contact())"""


