from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

def get_db_connection():
    connection_string = os.environ.get('postgresql://neondb_owner:npg_PnW0fdxZEu7w@ep-little-darkness-a4xktv4f-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require')
    if not connection_string:
        connection_string = "postgresql://neondb_owner:npg_PnW0fdxZEu7w@ep-little-darkness-a4xktv4f-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
    
    result = urlparse(connection_string)
    conn = psycopg2.connect(
        host=result.hostname,
        database=result.path[1:], 
        user=result.username,
        password=result.password,
        port=result.port
    )
    return conn

def release_db_connection(conn):
    """Close the database connection safely"""
    if conn:
        conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/members')
def members_all():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, batch FROM public.name ORDER BY name")
    members = cursor.fetchall()
    cursor.close()
    release_db_connection(conn)
    return render_template('members/all.html', members=members)

@app.route('/members/domain')
def members_domain_selection():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT domain FROM public.name WHERE domain IS NOT NULL ORDER BY domain")
    domains = cursor.fetchall()
    cursor.close()
    release_db_connection(conn)
    return render_template('members/domain.html', domains=domains)

@app.route('/members/domain/<domain>')
def members_by_domain(domain):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, batch FROM public.name WHERE domain = %s ORDER BY name", (domain,))
    members = cursor.fetchall()
    cursor.close()
    release_db_connection(conn)
    return render_template('members/all.html', members=members, selected_domain=domain)

@app.route('/members/details/<name>')
def member_details(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    

    cursor.execute("SELECT name.id FROM public.name WHERE name = %s", (name,))
    uuid_result = cursor.fetchone()
    
    if not uuid_result:
        cursor.close()
        release_db_connection(conn)
        return "Member not found", 404
    
    uuid = uuid_result[0]
    
    cursor.execute("SELECT name, batch, domain FROM public.name WHERE name.id = %s", (uuid,))
    basic_details = cursor.fetchone()
    
    cursor.execute("SELECT * FROM public.personal_details WHERE personal_details.id = %s", (uuid,))
    columns = [desc[0] for desc in cursor.description]
    personal_details_result = cursor.fetchone()
    
    personal_details = {}
    if personal_details_result:
        for i, col in enumerate(columns):
            if col.lower() != 'uuid':
                personal_details[col] = personal_details_result[i]
    
    cursor.execute("""
        SELECT camera_brand, camera_model, camera_id, lenses, sd_card_size, accessories 
        FROM public.cameras 
        WHERE cameras.id = %s
    """, (uuid,))
    camera_details = cursor.fetchall()
    
    cursor.close()
    release_db_connection(conn)
    
    return render_template('members/details.html', 
                          name=basic_details[0], 
                          batch=basic_details[1], 
                          domain=basic_details[2],
                          personal_details=personal_details,
                          camera_details=camera_details)

@app.route('/cameras')
def cameras():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.camera_brand, c.camera_model, c.camera_id, c.lenses, c.sd_card_size, c.accessories, n.name 
        FROM public.cameras c
        LEFT JOIN public.name n ON c.id = n.id
        ORDER BY c.camera_brand, c.camera_model
    """)
    cameras = cursor.fetchall()
    cursor.close()
    release_db_connection(conn)
    return render_template('cameras/list.html', cameras=cameras)

@app.route('/events')
def events():
    return render_template('events/list.html')

if __name__ == '__main__':
    app.run(debug=True)
