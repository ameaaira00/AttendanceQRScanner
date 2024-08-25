from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate/<event>", methods=["GET"])
def show_form(event):
    if event in ["Heads Monthly Meeting", "General SADP PYM Events"]:
        return render_template("form.html", event=event)
    else:
        return render_template("inprogress.html")


@app.route("/generate/<event>", methods=["POST"])
def generate(event):
    name = request.form["name"]
    data = f"Event: {event}, Participant: {name}"
    img = qrcode.make(data)

    # Save generated QR code
    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    # Encode QR code image to base64
    qr_code_img = base64.b64encode(img_io.getvalue()).decode("utf-8")

    return render_template("result.html", qr_code_img=qr_code_img, event=event)


if __name__ == "__main__":
    app.run(debug=True)
