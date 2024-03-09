import pyodbc

# Configuración de la conexión a la base de datos SQL Server
server = 'LAPTOP-JG6RLSQO'  # Nombre del servidor SQL Server
database = 'FIRPLAKSA'  # Nombre de la base de datos

def consultar_entregas():
    entregas = []
    try:
        # Establecer la conexión a la base de datos
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
        cursor = connection.cursor()

        # Ejecutar la consulta SQL para obtener las entregas
        cursor.execute('SELECT * FROM Entregas')

        # Recorrer los resultados y guardarlos en una lista de diccionarios
        for row in cursor.fetchall():
            entrega = {
                'Numero_Guia_Transporte': row[0],
                'Fecha_Despacho': row[1],
                'Cliente': row[2],
                'Destino': row[3],
                # Agregar más campos según la estructura de la tabla
            }
            entregas.append(entrega)
    except Exception as e:
        print("Error al consultar las entregas:", e)
    finally:
        cursor.close()
        connection.close()
    return entregas
