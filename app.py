from flask import Flask, request, render_template
from datetime import datetime
from pymongo import MongoClient


def create_app():
    app = Flask(__name__)

    # client agora é um cluster
    client = MongoClient("mongodb+srv://fabio:osCU8R1kcovVuIPt@cluster0.b8x2t.mongodb.net/test")

    # client.microblog é a base de dados que criamos sobre o cluster acima
    # adicionaremos esta base de dados a base de dados do nosso app
    app.db = client.microblog

    @app.route('/', methods=['GET', 'POST'])
    def home():
        # app.db.entries.find({}) seria a collection entries na base de dados salva agora em app.db que criamos no mongodb 
        # find({}) -> encontra tudo dentro da entries collection
        # print([x for x in app.db.entries.find()])
    
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.today().strftime("%Y-%m-%d")
            
            app.db.entries.insert({
                "content": entry_content,
                "date": formatted_date
                })
        
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
                # datetime.today().strftime("%b %d") -> mais fácil desta forma!!! - curso usou a linha de cima
            )
            for entry in app.db.entries.find({})
            # tuple comprehension
        ]
        return render_template("home.html", entries=entries_with_date)

    @app.route('/teste', methods=['GET', 'POST'])
    def teste():
        # app.db.entries.find({}) seria a collection entries na base de dados salva agora em app.db que criamos no mongodb 
        # find({}) -> encontra tudo dentro da entries collection
        lista_dados = list(app.db.entries.find())

        return render_template("teste.html", lista_dados=lista_dados)
    
    return app
