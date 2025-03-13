from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_db_connection():
    # Ajusta la conexión a tu base de datos
    conn = psycopg2.connect(
        host='localhost',
        database='alumnosinfocal',  # Tu base de datos
        user='admin',              # Usuario
        password='12345678'        # Contraseña
    )
    return conn

@app.route('/')
def home():
    """Ruta principal: redirige a /cards."""
    return redirect(url_for('cards'))

@app.route('/cards')
def cards():
    """
    Muestra a los alumnos en formato de "cards".
    Calcula el promedio de las calificaciones en calificacionesalumnos.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    # LEFT JOIN para mostrar todos los alumnos, incluso sin calificaciones.
    # Si solo quieres mostrar alumnos con calificaciones, usa INNER JOIN.
    cur.execute("""
        SELECT d.id_alumno, d.nombre, d.apellido, d.carrera, AVG(c.numero) as promedio
        FROM datosalumnos d
        LEFT JOIN calificacionesalumnos c ON d.id_alumno = c.id_alumno
        WHERE d.is_active = TRUE
        GROUP BY d.id_alumno, d.nombre, d.apellido, d.carrera
        ORDER BY d.id_alumno;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    alumnos = []
    for row in rows:
        # row = (id_alumno, nombre, apellido, carrera, promedio)
        alumno = {
            'id': row[0],
            'nombre': row[1],
            'apellido': row[2],
            'carrera': row[3],
            'promedio': round(row[4], 2) if row[4] is not None else None
        }
        alumnos.append(alumno)

    return render_template('cards.html', alumnos=alumnos)

@app.route('/add', methods=['GET', 'POST'])
def add_alumno():
    """Inserta un nuevo alumno en la tabla datosalumnos."""
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        direccion = request.form['direccion'].strip()
        fecha_nacimiento = request.form['fecha_nacimiento'].strip() or None
        carrera = request.form['carrera'].strip()
        telefono = request.form['telefono'].strip()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO datosalumnos (nombre, apellido, direccion, fecha_de_nacimiento, carrera, telefono, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE)
            RETURNING id_alumno;
        """, (nombre, apellido, direccion, fecha_nacimiento, carrera, telefono))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('cards'))
    else:
        return render_template('add.html')

@app.route('/edit/<int:alumno_id>', methods=['GET', 'POST'])
def edit_alumno(alumno_id):
    """Edita un alumno existente en la tabla datosalumnos."""
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        # Procesar la actualización
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        direccion = request.form['direccion'].strip()
        fecha_nacimiento = request.form['fecha_nacimiento'].strip() or None
        carrera = request.form['carrera'].strip()
        telefono = request.form['telefono'].strip()

        cur.execute("""
            UPDATE datosalumnos
            SET nombre = %s,
                apellido = %s,
                direccion = %s,
                fecha_de_nacimiento = %s,
                carrera = %s,
                telefono = %s
            WHERE id_alumno = %s;
        """, (nombre, apellido, direccion, fecha_nacimiento, carrera, telefono, alumno_id))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('cards'))
    else:
        # Mostrar formulario con datos actuales
        cur.execute("""
            SELECT id_alumno, nombre, apellido, direccion, fecha_de_nacimiento, carrera, telefono
            FROM datosalumnos
            WHERE id_alumno = %s;
        """, (alumno_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            alumno = {
                'id': row[0],
                'nombre': row[1],
                'apellido': row[2],
                'direccion': row[3],
                'fecha_nacimiento': row[4],
                'carrera': row[5],
                'telefono': row[6]
            }
            return render_template('edit.html', alumno=alumno)
        else:
            return "Alumno no encontrado", 404

@app.route('/delete/<int:alumno_id>', methods=['POST'])
def delete_alumno(alumno_id):
    """Elimina (o desactiva) un alumno por ID."""
    conn = get_db_connection()
    cur = conn.cursor()
    # Opción 1: eliminar físicamente
    # cur.execute("DELETE FROM datosalumnos WHERE id_alumno = %s;", (alumno_id,))
    
    # Opción 2: desactivar el registro (recomendado para conservar historial)
    cur.execute("""
        UPDATE datosalumnos
        SET is_active = FALSE
        WHERE id_alumno = %s;
    """, (alumno_id,))
    
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('cards'))

if __name__ == '__main__':
    app.run(debug=True)
