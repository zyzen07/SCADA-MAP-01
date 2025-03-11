from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import mysql.connector
from werkzeug.utils import secure_filename

# Flask Configurations
app = Flask(__name__)
app.secret_key = "secret_key"
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",         # Replace with your MySQL username
    password="Selva@1234", # Replace with your MySQL password
    database="ip_topology"
)
cursor = db.cursor()

# Ensure 'uploads' folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Route: Real-Time Dashboard
@app.route("/")
def dashboard():
    # Fetch devices and their connections
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()

    cursor.execute("SELECT * FROM connections")
    connections = cursor.fetchall()

    return render_template("dashboard.html", devices=devices, connections=connections)

# Route: Add Topology Form
@app.route("/add_topology", methods=["GET", "POST"])
def add_topology():
    if request.method == "POST":
        device_name = request.form["device_name"]
        ip_address = request.form["ip_address"]
        mac_address = request.form["mac_address"]
        interface = request.form["interface"]
        os_info = request.form["os"]
        status = request.form["status"]
        protocol = request.form["protocol"]

        # Handle file upload
        image_path = ""
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)

        # Insert data into MySQL
        cursor.execute("""
            INSERT INTO devices (device_name, image_path, ip_address, mac_address, interface, os, status, protocol)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (device_name, image_path, ip_address, mac_address, interface, os_info, status, protocol))
        db.commit()

        # Get the ID of the newly inserted device
        cursor.execute("SELECT id FROM devices ORDER BY id DESC LIMIT 1")
        new_device_id = cursor.fetchone()[0]

        # Automatically link the new device to all existing devices
        cursor.execute("SELECT id FROM devices WHERE id != %s", (new_device_id,))
        existing_devices = cursor.fetchall()
        for device in existing_devices:
            cursor.execute("""
                INSERT INTO connections (source_device_id, target_device_id)
                VALUES (%s, %s)
            """, (new_device_id, device[0]))
        db.commit()

        flash("Topology stored successfully!")
        return redirect(url_for("dashboard"))

    return render_template("add_topology.html")

# API Route: Fetch Devices and Connections for D3.js
@app.route("/api/topology", methods=["GET"])
def api_topology():
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()

    cursor.execute("SELECT * FROM connections")
    connections = cursor.fetchall()

    data = {
        "nodes": [{"id": d[0], "name": d[1], "image": d[2]} for d in devices],
        "links": [{"source": c[1], "target": c[2]} for c in connections]
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
