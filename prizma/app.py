from flask import Flask, render_template

app = Flask(__name__)

@app.get("/hello")
def hello():
    return render_template("hello.html")

@app.get("/header")
def header_page():
    # header.html est un document HTML complet (<!doctype html>)
    # placé dans templates/header.html
    return render_template("header.html", brand="Prizma")

@app.get("/footer")
def footer_page():
    # footer.html doit être dans templates/footer.html
    return render_template("footer.html")

@app.get("/")
def index():
    return "Accueil — placeholder"

@app.get("/produits")
def produits():
    return "Produits — placeholder"

@app.get("/contact")
def contact():
    return "Contact — placeholder"

@app.get("/auth")
def auth():
    return "Se connecter / Créer un compte — placeholder"

@app.get("/rgpd")
def rgpd(): return "RGPD — placeholder"

@app.get("/mentions-legales")
def mentions(): return "Mentions légales — placeholder"

@app.get("/cookies")
def cookies(): return "Cookies — placeholder"

if __name__ == "__main__":
    app.run(debug=True)
