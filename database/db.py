import psycopg2
from psycopg2 import pool
from config import DB_CONFIG

connection_pool = None

def init_db_pool():
    """Initialize database connection pool"""
    global connection_pool
    if connection_pool is None:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 10,
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database']
        )
    return connection_pool

def get_db_connection():
    """Get a connection from the pool"""
    global connection_pool
    if connection_pool is None:
        init_db_pool()
    return connection_pool.getconn()

def release_db_connection(conn):
    """Return a connection to the pool"""
    global connection_pool
    if connection_pool:
        connection_pool.putconn(conn)

def close_db_pool():
    """Close all connections in the pool"""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        connection_pool = None

# Member queries
def get_all_members():
    """Get all members from the name table"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name, batch FROM public.name ORDER BY name")
        members = cursor.fetchall()
        return members
    except Exception as e:
        print(f"Database error: {e}")
        return []
    finally:
        cursor.close()
        release_db_connection(conn)

def get_member_domains():
    """Get all unique domains from the name table"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT DISTINCT domain FROM public.name WHERE domain IS NOT NULL ORDER BY domain")
        domains = cursor.fetchall()
        return domains
    except Exception as e:
        print(f"Database error: {e}")
        return []
    finally:
        cursor.close()
        release_db_connection(conn)

def get_members_by_domain(domain):
    """Get members filtered by domain"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name, batch FROM public.name WHERE domain = %s ORDER BY name", (domain,))
        members = cursor.fetchall()
        return members
    except Exception as e:
        print(f"Database error: {e}")
        return []
    finally:
        cursor.close()
        release_db_connection(conn)

def get_member_by_name(name):
    """Get member UUID by name"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT uuid FROM public.name WHERE name = %s", (name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        release_db_connection(conn)

def get_member_details(uuid):
    """Get complete member details by UUID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Basic details
        cursor.execute("SELECT name, batch, domain FROM public.name WHERE uuid = %s", (uuid,))
        basic_details = cursor.fetchone()
        
        if not basic_details:
            return None
        
        # Personal details
        cursor.execute("SELECT * FROM public.personal_details WHERE uuid = %s", (uuid,))
        columns = [desc[0] for desc in cursor.description]
        personal_details_result = cursor.fetchone()
        
        # Filter out UUID
        personal_details = {}
        if personal_details_result:
            for i, col in enumerate(columns):
                if col.lower() != 'uuid':
                    personal_details[col] = personal_details_result[i]
        
        # Camera details
        cursor.execute("""
            SELECT camera_brand, camera_model, camera_id, lenses, sd_card_size, accessory 
            FROM public.cameras 
            WHERE uuid = %s
        """, (uuid,))
        camera_details = cursor.fetchall()
        
        return {
            'basic': {
                'name': basic_details[0],
                'batch': basic_details[1],
                'domain': basic_details[2]
            },
            'personal': personal_details,
            'cameras': camera_details
        }
    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        release_db_connection(conn)

# Camera queries
def get_all_cameras():
    """Get all cameras with owner information"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT c.camera_brand, c.camera_model, c.camera_id, c.lenses, c.sd_card_size, c.accessory, n.name 
            FROM public.cameras c
            LEFT JOIN public.name n ON c.uuid = n.uuid
            ORDER BY c.camera_brand, c.camera_model
        """)
        cameras = cursor.fetchall()
        return cameras
    except Exception as e:
        print(f"Database error: {e}")
        return []
    finally:
        cursor.close()
        release_db_connection(conn)
