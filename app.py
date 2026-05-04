from flask import Flask, render_template, request, session, redirect
import random
import time

app = Flask(__name__)
app.secret_key = "forca_final_123"

# 📚 categorias
PALAVRAS = {
    "animais": ["gato", "elefante", "tigre", "girafa", "leao", "urso", "panda", "jacare", "macaco"],
    "frutas": ["banana", "maca", "uva", "manga", "abacaxi", "pera", "morango", "melancia"],
    "paises": ["brasil", "portugal", "canada", "japao", "holanda", "espanha", "mexico", "egito", "alemanha", "haiti"]
}

MAX_ERROS = 6


# 🎮 MENU INICIAL
@app.route("/")
def menu():
    return render_template("menu.html")


# 🚀 INICIAR JOGO
@app.route("/start/<categoria>")
def start(categoria):

    palavra = random.choice(PALAVRAS[categoria])

    session["palavra"] = palavra
    session["categoria"] = categoria
    session["letras"] = []
    session["erros"] = 0
    session["pontos"] = 0
    session["inicio"] = time.time()

    return redirect("/game")


# 🎮 JOGO
@app.route("/game", methods=["GET", "POST"])
def game():

    if "palavra" not in session:
        return redirect("/")

    palavra = session["palavra"]

    if request.method == "POST":
        letra = request.form.get("letra")

        if letra and letra not in session["letras"]:
            session["letras"].append(letra)

            if letra in palavra:
                session["pontos"] += 10
            else:
                session["erros"] += 1
                session["pontos"] -= 5

    palavra_mostrada = " ".join(
        [l if l in session["letras"] else "_" for l in palavra]
    )

    tempo = int(time.time() - session["inicio"])

    ganhou = "_" not in palavra_mostrada
    perdeu = session["erros"] >= MAX_ERROS

    return render_template(
        "game.html",
        palavra=palavra_mostrada,
        letras=session["letras"],
        erros=session["erros"],
        max_erros=MAX_ERROS,
        pontos=session["pontos"],
        tempo=tempo,
        dificuldade=session["categoria"],
        ganhou=ganhou,
        perdeu=perdeu,
        palavra_real=palavra
    )


# 🔄 RESET
@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)