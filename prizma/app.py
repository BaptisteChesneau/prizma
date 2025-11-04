from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "dev-secret"  # requis si tu ajoutes du flash plus tard

# --- stockage éphémère en mémoire (facultatif) ---
USERS = []  # perdu à chaque redémarrage

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

# Produits
@app.get("/produits")
def produits():
    return render_template("products.html")  # garde ton nom de fichier

# -------- Auth: Se connecter / Créer un compte (sans DB) --------
@app.get("/auth")
def auth():
    # Affiche le formulaire d'inscription
    return render_template("auth.html", errors=[], success=False, form={}, created=None)

@app.post("/auth/create")
def auth_create():
    # Récupère les champs
    data = {
        "prenom": request.form.get("prenom", "").strip(),
        "nom": request.form.get("nom", "").strip(),
        "email": request.form.get("email", "").strip(),
        "adresse": request.form.get("adresse", "").strip(),
        "code_postal": request.form.get("code_postal", "").strip(),
        "ville": request.form.get("ville", "").strip(),
        "telephone": request.form.get("telephone", "").strip(),
    }

    # Validations simples
    errors = []
    if not data["prenom"]: errors.append("Le prénom est requis.")
    if not data["nom"]: errors.append("Le nom est requis.")
    if not data["email"] or "@" not in data["email"]:
        errors.append("L’adresse e-mail n’est pas valide.")
    if not data["adresse"]: errors.append("L’adresse postale est requise.")
    if not (data["code_postal"].isdigit() and len(data["code_postal"]) == 5):
        errors.append("Le code postal doit contenir 5 chiffres.")
    if not data["ville"]: errors.append("La ville est requise.")
    if not data["telephone"]:
        errors.append("Le numéro de téléphone est requis.")

    if errors:
        return render_template("auth.html", errors=errors, success=False, form=data, created=None)

    # Sans base : on conserve en mémoire (optionnel)
    USERS.append(data)
    return render_template("auth.html", errors=[], success=True, form={}, created=data)

# -------- Stubs de navigation --------
@app.get("/contact")
def contact():
    return "Contact — placeholder"

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
