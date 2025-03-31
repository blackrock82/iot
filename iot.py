from flask import Flask, request

app = Flask(__name__)

@app.route('/rfid', methods=['GET'])
def get_rfid():
    rfid_uid = request.args.get('uid')
    if rfid_uid:
        print(f"Received RFID UID: {rfid_uid}")
        return {"status": "success", "rfid": rfid_uid}
    return {"status": "error", "message": "No UID provided"}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)