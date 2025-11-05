from flask import Flask, render_template, send_file
from io import BytesIO
from loyalty_card import generate_loyalty_card

app = Flask(__name__)

@app.get("/hello")
def hello():
    return render_template("hello.html")

@app.route("/mentions-legales/")
def legal_notices():
    return render_template("legal_notices.html")

@app.route("/politique-cookies/")
def cookies_policy():
    return render_template("cookies_policy.html")

@app.route("/mon-compte/")
def account():
    return render_template("account.html")

@app.route("/fidelite/<member_id>")
def fidelite(member_id):
    # Générer la carte
    card = generate_loyalty_card(member_id)
    
    # Mettre l'image en mémoire
    buf = BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
