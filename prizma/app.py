from flask import Flask, render_template

app = Flask(__name__)

# Accueil = home.html
@app.get("/")
def home():
    return render_template("home.html")  # <-- pas d'index.html

@app.get("/hello")
def hello():
    return render_template("hello.html")

# (Facultatif) aperçu des fragments si tu veux les voir seuls
@app.get("/header")
def header_fragment():
    return render_template("header.html")

@app.get("/footer")
def footer_fragment():
    return render_template("footer.html")

@app.get("/produits")
def produits():
    return render_template("products.html")

# Stubs de navigation

@app.get("/contact")
def contact():
    return "Contact — placeholder"

@app.get("/auth")
def auth():
    return "Se connecter / Créer un compte — placeholder"

@app.get("/rgpd")
def rgpd():
    return "RGPD — placeholder"

@app.get("/mentions-legales")
def mentions():
    return "Mentions légales — placeholder"

@app.get("/cookies")
def cookies():
    return "Cookies — placeholder"

if __name__ == "__main__":
    app.run(debug=True)
