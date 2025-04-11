from flask import Flask, request, jsonify, render_template
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
application = app
# Database Configuration
#idezignmedia.co.zw
DB_CONFIG = {
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# SQLAlchemy Engine (alternative connection method)
try:
    engine = create_engine(f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")
except Exception as e:
    print(f"Error creating engine: {e}")
    engine = None

def check_rfid_in_db(tag_id):
    """Check if RFID exists in database"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as count FROM rfid_tags WHERE tag_id = %s"
            cursor.execute(sql, (tag_id,))
            result = cursor.fetchone()
            return result['count'] > 0
    except pymysql.Error as err:
        print(f"Database error: {err}")
        return False
    finally:
        if 'connection' in locals() and connection:
            connection.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['GET'])
def verify():
    rfid_uid = request.args.get('uid')
    if not rfid_uid:
        return jsonify({"error": "Missing RFID UID parameter"}), 400

    try:
        is_valid = check_rfid_in_db(rfid_uid)
        if is_valid:
            return jsonify({
                "status": "success",
                "message": f"RFID Tag {rfid_uid} is valid",
                "data": {"uid": rfid_uid}
            }), 200
        else:
            return jsonify({
                "status": "not_found",
                "message": f"RFID Tag {rfid_uid} not found in database"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
