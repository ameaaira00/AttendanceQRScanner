import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import qrcode
import io
import base64
from events import EventType


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate/<event>", methods=["GET"])
def show_form(event):
    try:
        # Validate the event against the enum
        EventType(event)
    except ValueError:
        return render_template("inprogress.html")

    if event in ["Heads Monthly Meeting", "General SADP PYM Events"]:
        return render_template("form.html", event=event)
    else:
        return render_template("inprogress.html")


@app.route("/generate/<event>", methods=["POST"])
def generate(event):
    name = request.form["name"]

    # Check if the participant already exists in the database
    qr_code_img = get_qr_code(event, name)

    # If the participant does not exist, generate a new QR code
    if not qr_code_img:
        data = f"{event},{name}"
        img = qrcode.make(data)

        # Save generated QR code to memory
        img_io = io.BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)

        # Encode the QR code image to base64
        qr_code_img = base64.b64encode(img_io.getvalue()).decode("utf-8")

        # Save the new participant and QR code in the database
        save_participant(event, name, qr_code_img)

    # Render the result page with the QR code
    return render_template("result.html", qr_code_img=qr_code_img, event=event)


# Function to save a participant
def save_participant(event, name, qr_code_img):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO participants (event, name, qr_code) VALUES (?, ?, ?)",
            (event, name, qr_code_img),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # Handle unique constraint violation (duplicate entry)
        pass
    conn.close()


# Function to check if a participant already exists
def get_qr_code(event, name):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT qr_code FROM participants WHERE event = ? AND name = ?", (event, name)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


@app.route("/scan", methods=["GET"])
def scan_form():
    return render_template("scan.html")


@app.route("/scan", methods=["POST"])
def scan():
    scan_data = request.form.get("scan_data")

    if not scan_data:
        message = "No scan data provided."
        success = False
    else:
        event, name = parse_scan_data(scan_data)

        if not event or not name:
            message = "Invalid scan data format."
            success = False
        else:
            # Check if the participant exists in the database
            if participant_exists(event, name):
                save_scan(event, name)
                message = "Scan recorded successfully!"
                success = True
            else:
                message = "Invalid event or participant."
                success = False

    return render_template("scan.html", message=message, success=success)


def parse_scan_data(scan_data):
    try:
        event, name = scan_data.split(",", 1)
        return event.strip(), name.strip()
    except ValueError:
        return None, None


def participant_exists(event, name):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM participants WHERE event = ? AND name = ?",
        (event, name),
    )
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists


def save_scan(event, name):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scans (event, name, scan_time) VALUES (?, ?, datetime('now'))",
        (event, name),
    )
    conn.commit()
    conn.close()


@app.route("/admin")
def admin_home():
    events = [event.value for event in EventType]
    return render_template("admin_home.html", events=events)


@app.route("/admin/<event>", methods=["GET"])
def admin_event(event):
    try:
        EventType(event)  # Ensure valid event type
    except ValueError:
        return redirect(url_for("admin_home"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name, scan_time
        FROM scans
        WHERE event = ?
    """,
        (event,),
    )
    scanned_participants = cursor.fetchall()
    conn.close()

    return render_template(
        "admin_event.html", event=event, scanned_participants=scanned_participants
    )


if __name__ == "__main__":
    app.run(debug=True)
