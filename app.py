# Importaciones necesarias
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pyodbc

# Creación de la aplicación Flask
app = Flask(__name__)

# Configuración de la conexión a la base de datos SQL Server
server = 'LAPTOP-JG6RLSQO'  # Nombre del servidor SQL Server
database = 'FIRPLAKSA'  # Nombre de la base de datos

# Función para verificar si ya existe una entrega con el mismo número de guía
def verificar_numero_guia(numero_guia):
    try:
        # Establecer la conexión a la base de datos
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
        cursor = connection.cursor()

        # Verificar si ya existe una entrega con el mismo número de guía
        cursor.execute("SELECT COUNT(*) FROM Entregas WHERE Numero_Guia_Transporte=?", (numero_guia,))
        count = cursor.fetchone()[0]

        return count > 0
    except Exception as e:
        print(f"Error al verificar el número de guía: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

# Vista para mostrar el formulario de entrega
@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

# Vista para manejar la solicitud de agregar una entrega
@app.route('/agregar_entrega', methods=['POST'])
def agregar_entrega():
    connection = None
    cursor = None
    try:
        # Obtener los datos del formulario
        numero_guia = request.form['numero_guia']
        numero_documento = request.form['numero_documento']
        fecha_despacho = request.form['fecha_despacho']
        cliente = request.form['cliente']
        destino = request.form['destino']
        fecha_entrega = request.form['fecha_entrega']
        estado_entrega = request.form['estado_entrega']
        tipo_transportadora = request.form['tipo_transportadora']
        pod_recibido = True if 'pod_recibido' in request.form else False
        observaciones = request.form['observaciones']

        # Verificar si ya existe una entrega con el mismo número de guía
        if verificar_numero_guia(numero_guia):
            return jsonify({"error": "Ya existe una entrega con este número de guía."}), 400

        # Establecer la conexión a la base de datos
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
        cursor = connection.cursor()

        # Insertar la entrega en la base de datos
        cursor.execute("INSERT INTO Entregas (Numero_Guia_Transporte, Numero_Documento_Entrega, Fecha_Despacho, Cliente, Destino, Fecha_Entrega, Estado_Entrega, Tipo_Transportadora, POD_Recibido, Observaciones) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (numero_guia, numero_documento, fecha_despacho, cliente, destino, fecha_entrega, estado_entrega, tipo_transportadora, pod_recibido, observaciones))
        
        connection.commit()
        return 'Entrega agregada exitosamente'
    except Exception as e:
        return f"Error al agregar entrega: {e}", 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

# Vista para mostrar la lista de entregas
@app.route('/')
def index():
    try:
        # Establecer la conexión a la base de datos
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
        cursor = connection.cursor()

        # Obtener los datos de todas las entregas
        cursor.execute("SELECT * FROM Entregas")
        entregas = cursor.fetchall()

        # Verificar si hay un indicador de actualización y pasarlo a la plantilla
        actualizado = request.args.get('actualizado')

        return render_template('index.html', entregas=entregas, actualizado=actualizado)
    except Exception as e:
        return f"Error al obtener los datos de las entregas: {e}"
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

# Vista para eliminar una entrega
@app.route('/borrar_entrega/<int:entrega_id>', methods=['POST'])
def borrar_entrega(entrega_id):
    try:
        # Establecer la conexión a la base de datos
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
        cursor = connection.cursor()

        # Eliminar la entrega de la base de datos
        cursor.execute("DELETE FROM Entregas WHERE ID_Entrega=?", (entrega_id,))
        connection.commit()

        return redirect(url_for('index'))  # Redirigir al index después de eliminar la entrega
    except Exception as e:
        return f"Error al eliminar la entrega: {e}"
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

# Vista para actualizar el estado de una entrega
@app.route('/actualizar_estado/<int:entrega_id>', methods=['POST'])
def actualizar_estado(entrega_id):
    try:
        # Establecer la conexión a la base de datos
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
        cursor = connection.cursor()

        # Obtener el estado actual de la entrega
        cursor.execute("SELECT Estado_Entrega FROM Entregas WHERE ID_Entrega=?", (entrega_id,))
        estado_actual = cursor.fetchone()[0]

        # Actualizar el estado solo si no es "Entrega exitosa"
        if estado_actual != 'Entrega exitosa':
            nuevo_estado = 'Entrega exitosa'  # Cambiar aquí el nuevo estado deseado
            cursor.execute("UPDATE Entregas SET Estado_Entrega=? WHERE ID_Entrega=?", (nuevo_estado, entrega_id))
            connection.commit()

            # Redirigir de nuevo al index con un indicador de éxito
            return redirect(url_for('index', actualizado=True))
        else:
            # Redirigir al index sin hacer cambios si el estado es "Entrega exitosa"
            return redirect(url_for('index'))
    except Exception as e:
        return f"Error al actualizar el estado de la entrega: {e}"
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

# Ejecutar la aplicación si este archivo es el principal
if __name__ == '__main__':
    app.run(debug=True)
