#!usr/bin/python3
from flask import Flask
import jsonify
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)

#MySQL configuration
app.config['MYSQL_USER'] = 'telemetryuser'
app.config['MYSQL_PASSWORD'] = 'telemetryuser123'
app.config['MYSQL_DB'] = 'telemetryDB'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/telemetry/<string:date>", methods=['GET'])
def get_telemetry():
    telemetry = request.get_json()
    print(telemetry)

    conn = mysql.connect
    cursor = conn.cursor()
	
	From = request.args.get('From')
	to = request.args.get('to')
	if From is None or to is None:
		cursor.execute("SELECT * FROM Measurement")
	else:
		cmd = "SELECT * FROM Measurement WHERE CreatedOn BETWEEN %s AND %s"
    	params = (From, to)
		cursor.execute(cmd, params)
    rows = cursor.fetchall()
	return jsonify({'telemetry': rows})

@app.route("/telemetry", methods=['POST'])
def add_telemetry():
	new_data = request.get_json()
    print(new_data)
	
    conn = mysql.connect
    cursor = conn.cursor()
    
	cmd = "INSERT INTO Measurement (MeasurementId, DeviceId, SensorName, SensorValue ,CreatedOn)"
    values = "VALUES (NULL, %s , %s, %s , %s)"
	
    cmd = cmd + values
    
    params = (new_data['DeviceId'], new_data['SensorName'], new_data['SensorValue'], new_data['CreatedOn'])
    cursor.execute(cmd, params)
    
	conn.commit()
    cursor.close()
    
	return "200"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
