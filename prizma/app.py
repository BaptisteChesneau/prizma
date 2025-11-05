from flask import Flask, render_template, request, session, redirect, url_for
import unicodedata
import re

app = Flask(__name__)
app.secret_key = "dev-secret"  # requis si tu ajoutes du flash plus tard

# --- stockage éphémère en mémoire (facultatif) ---
USERS = []  # perdu à chaque redémarrage

# --------- Libellés des catégories (ids utilisés dans products.html) ----------
CATEGORY_LABELS = {
    "maison": "Maison & Jardin",
    "hightech": "Informatique & High-Tech",
    "tel": "Téléphonie & Objets connectés",
    "av": "Image & Son",
    "jeux": "Jeux vidéo & Consoles",
    "auto": "Auto, Moto & GPS",
    "mode": "Mode & Beauté",
    "bebe": "Bébé & Puériculture",
    "jouets": "Jouets & Enfants",
    "sport": "Sport & Loisirs",
    "voyage": "Voyage & Bagagerie",
    "animaux": "Animaux",
    "bureau": "Bureau & Fournitures",
    "supermarche": "Supermarché & Alimentation",
}

# --------- Mini-catalogue d'exemple (clé = slug de sous-catégorie) -----------
# NB : c'est un exemple minimal pour démontrer la navigation. Tu peux enrichir.
CATALOGUE = {
    "maison": {
        "meubles-decoration": [
            {"ref": "MD-001", "name": "Table basse en chêne", "price": 129.99},
            {"ref": "MD-002", "name": "Lampe sur pied scandinave", "price": 59.90},
        ],
        "linge-de-maison": [
            {"ref": "LM-010", "name": "Parure de lit coton 140x200", "price": 39.90},
        ],
        "electromenager": [
            {"ref": "EM-200", "name": "Bouilloire inox 1.7L", "price": 24.99},
        ],
        "bricolage-outillage": [
            {"ref": "BO-111", "name": "Perceuse-visseuse 18V", "price": 89.00},
        ],
        "jardin-terrasse-piscine": [
            {"ref": "JTP-005", "name": "Tuyau extensible 15m", "price": 29.90},
        ],
        "domotique-securite": [
            {"ref": "DS-300", "name": "Prise connectée Wi-Fi", "price": 14.90},
        ],
        "cuisine-arts-de-la-table": [
            {"ref": "CAT-021", "name": "Batterie de cuisine 5 pièces", "price": 79.00},
        ],
    },
    "hightech": {
        "ordinateurs-portables": [
            {"ref": "OP-001", "name": "Laptop 15\" i5 / 16 Go / 512 Go", "price": 749.00},
        ],
        "ecrans-moniteurs": [
            {"ref": "MON-027", "name": "Écran 27\" 144Hz", "price": 219.00},
        ],
        "imprimantes-scanners": [
            {"ref": "IMP-010", "name": "Imprimante Wi-Fi multifonction", "price": 69.00},
        ],
        "accessoires-claviers-souris-sacs": [
            {"ref": "ACC-501", "name": "Souris sans fil", "price": 14.90},
        ],
        "composants-peripheriques": [],
        "tablettes-liseuses": [],
    },
    "tel": {
        "smartphones": [
            {"ref": "SP-900", "name": "Smartphone 5G 128 Go", "price": 259.00},
        ],
        "accessoires-telephone": [
            {"ref": "TEL-030", "name": "Coque silicone (noir)", "price": 9.90},
        ],
        "montres-bracelets-connectes": [
            {"ref": "WB-070", "name": "Montre connectée étanche", "price": 49.90},
        ],
        "casques-ecouteurs": [
            {"ref": "AUD-100", "name": "Écouteurs Bluetooth", "price": 29.90},
        ],
        "batteries-chargeurs": [],
    },
    "av": {
        "televiseurs": [{"ref": "TV-050", "name": "TV 55\" 4K HDR", "price": 449.00}],
        "home-cinema-barres-de-son": [],
        "videoprojecteurs": [],
        "appareils-photo-cameras": [],
        "drones-accessoires": [],
    },
    # Tu peux compléter les autres catégories à ton rythme :
    "jeux": {},
    "auto": {},
    "mode": {},
    "bebe": {},
    "jouets": {},
    "sport": {},
    "voyage": {},
    "animaux": {},
    "bureau": {},
    "supermarche": {},
}

# --------- Utilitaire : slugify (cohérent avec le JS côté front) -------------
def slugify(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = s.replace("&", " ")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


# Accueil = home.html
@app.get("/")
def home():
    return render_template("home.html")  # <-- pas d'index.html


@app.get("/hello")
def hello():
    return render_template("hello.html")


# (Facultatif) aperçu des fragments
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
    if not data["prenom"]:
        errors.append("Le prénom est requis.")
    if not data["nom"]:
        errors.append("Le nom est requis.")
    if not data["email"] or "@" not in data["email"]:
        errors.append("L’adresse e-mail n’est pas valide.")
    if not data["adresse"]:
        errors.append("L’adresse postale est requise.")
    if not (data["code_postal"].isdigit() and len(data["code_postal"]) == 5):
        errors.append("Le code postal doit contenir 5 chiffres.")
    if not data["ville"]:
        errors.append("La ville est requise.")
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
    return redirect(url_for("signup"), code=301)

@app.post("/auth/create")
def auth_legacy_post():
    return redirect(url_for("signup_create"), code=307)


# -------- Connexion (sans DB) --------
@app.get("/login")
def login():
    me = session.get("user")
    if me:
        # déjà connecté → espace client
        return redirect(url_for("compte"))
    return render_template("login.html", errors=[], form={}, me=None, success=False)

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
        return render_template(
            "login.html",
            errors=errors,
            form={"email": email, "code_postal": code_postal},
            me=None,
            success=False
        )

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

    # OK : on "connecte" l'utilisateur en session (session complète pour /compte)
    session["user"] = {
        "prenom": me.get("prenom"),
        "nom": me.get("nom"),
        "email": me.get("email"),
        "adresse": me.get("adresse"),
        "code_postal": me.get("code_postal"),
        "ville": me.get("ville"),
        "telephone": me.get("telephone"),
    }
    # redirection immédiate vers l'espace client
    return redirect(url_for("compte"))


@app.get("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# -------- Espace client (/compte) --------
def _current_user():
    return session.get("user")

def _update_user_store(email, data):
    """Met à jour l'utilisateur correspondant dans USERS (en mémoire)."""
    for u in USERS:
        if u.get("email") == email:
            u.update(data)
            return True
    return False

@app.get("/compte")
def compte():
    me = _current_user()
    if not me:
        return redirect(url_for("login"))
    # success=None au premier affichage
    return render_template("account.html", me=me, errors=[], success=None)

@app.post("/compte/update")
def compte_update():
    me = _current_user()
    if not me:
        return redirect(url_for("login"))

    # On ne permet pas de changer l'email pour l’instant
    updated = {
        "prenom": request.form.get("prenom", "").strip(),
        "nom": request.form.get("nom", "").strip(),
        "adresse": request.form.get("adresse", "").strip(),
        "code_postal": request.form.get("code_postal", "").strip(),
        "ville": request.form.get("ville", "").strip(),
        "telephone": request.form.get("telephone", "").strip(),
    }

    errors = []
    if not updated["prenom"]:
        errors.append("Le prénom est requis.")
    if not updated["nom"]:
        errors.append("Le nom est requis.")
    if not updated["adresse"]:
        errors.append("L’adresse postale est requise.")
    if not (updated["code_postal"].isdigit() and len(updated["code_postal"]) == 5):
        errors.append("Le code postal doit contenir 5 chiffres.")
    if not updated["ville"]:
        errors.append("La ville est requise.")
    if not updated["telephone"]:
        errors.append("Le numéro de téléphone est requis.")

    if errors:
        me_view = {**me, **updated}
        return render_template("account.html", me=me_view, errors=errors, success=False)

    _update_user_store(me["email"], updated)
    session["user"] = {**session["user"], **updated}

    return render_template("account.html", me=session["user"], errors=[], success=True)


# -------- Pages catalogue dynamiques --------
@app.get("/catalogue/<category>/<subcat>")
def catalogue(category, subcat):
    """
    category = id de section (ex: 'maison', 'hightech', ...)
    subcat   = slug de la sous-catégorie (ex: 'meubles-decoration')
    """
    cat_items = CATALOGUE.get(category, {})
    # tente résolution directe puis fallback via slugify
    items = cat_items.get(subcat)
    if items is None:
        items = cat_items.get(slugify(subcat))
    if items is None:
        items = []  # sous-catégorie inconnue → page vide mais valide

    cat_label = CATEGORY_LABELS.get(category, category.title())
    # sous-label "humain"
    sub_label = subcat.replace("-", " ").capitalize()

    return render_template(
        "catalogue.html",
        category=category,
        subcat=subcat,
        cat_label=cat_label,
        sub_label=sub_label,
        items=items
    )


# -------- Contact --------
@app.get("/contact")
def contact():
    return render_template("contact.html")


# -------- Stubs de navigation --------
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
