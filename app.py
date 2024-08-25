import logging
from flask import Flask, render_template, request, send_file
import qrcode
import io


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template("generate.html")


# Generate QR code
@app.route("/generate", methods=["POST"])
def generate():
    event = request.form.get("event")
    name = request.form.get("name")

    app.logger.info(f"Event: {event}, Name: {name}")

    if not event or not name:
        app.logger.error("Error: Missing event or participant name")
        return "Error: Missing event or participant name", 400

    data = f"Event: {event}\nParticipant: {name}"
    app.logger.info(f"Generating QR code with data: {data}")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    app.logger.info("QR code generated successfully")
    return send_file(img_io, mimetype="image/png")


# Scan QR code
@app.route("/scan")
def scan():
    return render_template("scan.html")


if __name__ == "__main__":
    app.run(debug=True)
