from flask import Flask, render_template, request, session, redirect, url_for

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


# -------- Sign-up (ex-/auth) : Créer un compte (sans DB) --------
@app.get("/sign-up")
def signup():
    # Affiche le formulaire d'inscription
    return render_template("signup.html", errors=[], success=False, form={}, created=None)


@app.post("/sign-up/create")
def signup_create():
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
        return render_template("signup.html", errors=errors, success=False, form=data, created=None)

    # Sans base : on conserve en mémoire (optionnel)
    USERS.append(data)
    return render_template("signup.html", errors=[], success=True, form={}, created=data)


# -------- Legacy redirects (/auth → /sign-up) --------
@app.get("/auth")
def auth_legacy_get():
    # redirection permanente pour l'ancien chemin
    return redirect(url_for("signup"), code=301)

@app.post("/auth/create")
def auth_legacy_post():
    # conserve la méthode POST et le body
    return redirect(url_for("signup_create"), code=307)


# -------- Connexion (sans DB) --------
@app.get("/login")
def login():
    me = session.get("user")
    return render_template("login.html", errors=[], form={}, me=me, success=False)

@app.post("/login")
def login_post():
    email = request.form.get("email", "").strip()
    code_postal = request.form.get("code_postal", "").strip()

    errors = []
    if not email or "@" not in email:
        errors.append("L’adresse e-mail n’est pas valide.")
    if not (code_postal.isdigit() and len(code_postal) == 5):
        errors.append("Le code postal doit contenir 5 chiffres.")

    if errors:
        return render_template("login.html", errors=errors, form={"email": email, "code_postal": code_postal}, me=None, success=False)

    # Recherche d'un utilisateur correspondant (e-mail + code postal)
    me = next((u for u in USERS if u.get("email") == email and u.get("code_postal") == code_postal), None)
    if not me:
        return render_template(
            "login.html",
            errors=["Aucun compte ne correspond à cet e-mail / code postal."],
            form={"email": email, "code_postal": code_postal},
            me=None,
            success=False
        )

    # OK : on "connecte" l'utilisateur en session
    session["user"] = {
        "prenom": me.get("prenom"),
        "nom": me.get("nom"),
        "email": me.get("email"),
        "code_postal": me.get("code_postal"),
        "ville": me.get("ville"),
    }
    return render_template("login.html", errors=[], form={}, me=session["user"], success=True)


@app.get("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


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
