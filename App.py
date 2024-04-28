from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import database

app = Flask(__name__)

# Clave secreta para la sesión
app.secret_key = 'mysecretkey'

# Función para validar el formulario de inicio de sesión
def validar_formulario_login(email, password):
    if not email or not password:
        return False, "Por favor, complete todos los campos."
    # Aquí podrías agregar más validaciones, como verificar el formato del correo electrónico, longitud de la contraseña, etc.
    return True, None

# Ruta para la página de inicio de sesión (manejar solicitudes GET y POST)
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None  # Inicializamos la variable de error

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Validar el formulario
        es_valido, mensaje_error = validar_formulario_login(email, password)
        if not es_valido:
            return render_template('index.html', error=mensaje_error)
        
        # Verificar las credenciales en la base de datos
        cursor = database.cursor()
        cursor.execute('SELECT * FROM Estudiantes WHERE correo = %s AND contraseña = %s', (email, password))
        user = cursor.fetchone()

        if user:
            # Si las credenciales son correctas, establecer la sesión de usuario
            session['usuario'] = email
            return redirect(url_for('inicio'))
        else:
            # Si las credenciales son incorrectas, mostrar un mensaje de error
            error = "Usuario o contraseña incorrectos. Inténtalo de nuevo."

    return render_template('index.html', error=error)

# Ruta para la página de inicio después de iniciar sesión
@app.route('/inicio')
def inicio():
    # Verificar si el usuario está autenticado
    if 'usuario' in session:
        # Obtener las tareas desde la base de datos
        cursor = database.cursor()
        cursor.execute('SELECT * FROM Tareas')
        tareas = cursor.fetchall()
        return render_template('inicio.html', tareas=tareas)
    else:
        # Si el usuario no está autenticado, redirigirlo al inicio de sesión
        return redirect(url_for('index'))

# Ruta para cerrar sesión
@app.route('/cerrar_sesion')
def cerrar_sesion():
    # Remover el usuario de la sesión
    session.pop('usuario', None)
    return redirect(url_for('index'))

# Ruta para la página de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Guardar los datos en la base de datos
        cursor = database.cursor()
        cursor.execute('INSERT INTO Estudiantes (correo, contraseña) VALUES (%s, %s)', (email, password))
        database.commit()  # Guardar los cambios en la base de datos

        # Mensaje de éxito y redirección
        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('index'))

    return render_template('registrar.html')

# Ruta para agregar una tarea
@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    if request.method == 'POST':
        # Obtener los datos del formulario
        titulo = request.form['titulo']
        detalle = request.form['detalle']
        
        # Obtener el cursor desde la conexión existente
        cursor = database.cursor()
        
        # Ejecutar la consulta SQL para insertar la nueva tarea
        cursor.execute('INSERT INTO Tareas (titulo, detalle) VALUES (%s, %s)', (titulo, detalle))
        
        # Hacer commit para guardar los cambios en la base de datos
        database.commit()
        
        flash('Tarea agregada correctamente', 'success')
        
        # Redirigir al inicio después de agregar la tarea
        return redirect(url_for('inicio'))

# Ruta para eliminar una tarea
@app.route('/eliminar_tarea/<int:tarea_id>', methods=['POST'])
def eliminar_tarea(tarea_id):
    if request.method == 'POST':
        # Obtener el cursor desde la conexión existente
        cursor = database.cursor()
        # Ejecutar la consulta SQL para eliminar la tarea
        cursor.execute('DELETE FROM Tareas WHERE id = %s', (tarea_id,))
        # Hacer commit para guardar los cambios en la base de datos
        database.commit()
        flash('Tarea eliminada correctamente', 'success')
    return redirect(url_for('inicio'))

# Ruta raíz para mostrar las tareas
@app.route('/')
def Index():
    # Obtener las tareas desde la base de datos
    cursor = database.cursor()
    cursor.execute('SELECT * FROM Tareas')
    tareas = cursor.fetchall()
    return render_template('inicio.html', tareas=tareas)

# Corrida del programa
if __name__ == '__main__':
    app.run(port=4000, debug=True)
