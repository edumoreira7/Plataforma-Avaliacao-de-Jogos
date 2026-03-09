import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# ============================================================
# DESCOMENTE E INSTALE QUANDO FOR ADICIONAR OS OUTROS BANCOS:
# pip install psycopg2-binary pymongo redis
# ============================================================
# import psycopg2
# from pymongo import MongoClient
# import redis

app = Flask(__name__)
CORS(app)

# ============================================================
# ✅ NEO4J - CONFIGURADO E FUNCIONANDO
# ============================================================
NEO4J_HTTP = "https://696a2870.databases.neo4j.io/db/696a2870/query/v2"
NEO4J_USER = "696a2870"
NEO4J_PASS = "xb5P0RYACPcs4AZKhLxZ5Gk16Yt-GWuvpAXZuq150uY"

credentials = base64.b64encode(f"{NEO4J_USER}:{NEO4J_PASS}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json"
}

def run_query(cypher, params={}):
    payload = {"statement": cypher, "parameters": params}
    res = requests.post(NEO4J_HTTP, json=payload, headers=HEADERS)
    return res.json()

try:
    test = run_query("RETURN 1 AS ok")
    if test.get("errors"):
        print(f"❌ Neo4j erro: {test['errors']}")
    else:
        print("✅ Neo4j conectado com sucesso!")
except Exception as e:
    print(f"❌ Neo4j erro: {e}")

# ============================================================
# ⏳ POSTGRESQL (SUPABASE) - PREENCHER DEPOIS
# ============================================================
# POSTGRES_URL = "postgresql://postgres:SENHA@db.XXXX.supabase.co:5432/postgres"
#
# try:
#     pg_conn = psycopg2.connect(POSTGRES_URL)
#     cur = pg_conn.cursor()
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id SERIAL PRIMARY KEY,
#             name VARCHAR(100),
#             email VARCHAR(100) UNIQUE,
#             balance NUMERIC DEFAULT 0
#         );
#     """)
#     pg_conn.commit()
#     cur.close()
#     print("✅ PostgreSQL conectado com sucesso!")
# except Exception as e:
#     print(f"❌ PostgreSQL erro: {e}")
#     pg_conn = None

# ============================================================
# ✅ MONGODB (ATLAS)
# ============================================================
MONGO_URL = os.getenv("MONGO_URL")

try:
    mongo_client = MongoClient(MONGO_URL)
    mongo_db = mongo_client["gamehub"]

    # testa a conexão
    mongo_client.admin.command("ping")

    print("✅ MongoDB conectado com sucesso!")
except Exception as e:
    print(f"❌ MongoDB erro: {e}")
    mongo_db = None

# ============================================================
# ⏳ REDIS (UPSTASH) - PREENCHER DEPOIS
# ============================================================
# REDIS_URL = "rediss://default:SENHA@XXXX.upstash.io:6379"
#
# try:
#     redis_client = redis.from_url(REDIS_URL, decode_responses=True)
#     redis_client.ping()
#     print("✅ Redis conectado com sucesso!")
# except Exception as e:
#     print(f"❌ Redis erro: {e}")
#     redis_client = None

# ============================================================
# ROTAS - STATUS
# ============================================================

@app.route("/")
def home():
    try:
        test = run_query("RETURN 1 AS ok")
        neo4j_status = "✅ Conectado" if not test.get("errors") else "❌ Erro"
    except:
        neo4j_status = "❌ Desconectado"

    mongodb_status = "✅ Conectado" if mongo_db is not None else "❌ Desconectado"

    return jsonify({
        "backend": "GameHub Online",
        "neo4j": neo4j_status,
        "postgres": "⏳ Pendente - Supabase",
        "mongodb": mongodb_status,
        "redis": "⏳ Pendente - Upstash"
    })

# ============================================================
# ROTAS - NEO4J (AMIGOS) ✅
# ============================================================

@app.route("/friends", methods=["POST"])
def add_friend():
    try:
        data = request.json
        user1 = data.get("user1")
        user2 = data.get("user2")

        if not user1 or not user2:
            return jsonify({"error": "Informe user1 e user2"}), 400

        result = run_query("""
            MERGE (a:User {name: $u1})
            MERGE (b:User {name: $u2})
            MERGE (a)-[:FRIEND]->(b)
        """, {"u1": user1, "u2": user2})

        if result.get("errors"):
            return jsonify({"error": str(result["errors"])}), 500

        return jsonify({"status": f"✅ {user1} e {user2} agora são amigos no Neo4j!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/friends/<username>", methods=["GET"])
def get_friends(username):
    try:
        result = run_query(
            "MATCH (a:User {name: $name})-[:FRIEND]-(b:User) RETURN b.name AS friend",
            {"name": username}
        )
        rows = result.get("data", {}).get("values", [])
        friends = [r[0] for r in rows]
        return jsonify({"user": username, "friends": friends})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/nodes", methods=["GET"])
def get_all_nodes():
    try:
        result = run_query("MATCH (n) RETURN n.name AS name, labels(n) AS tipo")
        rows = result.get("data", {}).get("values", [])
        nodes = [{"name": r[0], "tipo": r[1]} for r in rows]
        return jsonify(nodes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# ROTAS - POSTGRESQL (USUÁRIOS) ⏳
# ============================================================

@app.route("/users", methods=["GET"])
def get_users():
    # DESCOMENTE QUANDO CONFIGURAR O POSTGRESQL
    # try:
    #     cur = pg_conn.cursor()
    #     cur.execute("SELECT id, name, email, balance FROM users")
    #     rows = cur.fetchall()
    #     cur.close()
    #     users = [{"id": r[0], "name": r[1], "email": r[2], "balance": str(r[3])} for r in rows]
    #     return jsonify(users)
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500
    return jsonify({"info": "⏳ PostgreSQL ainda não configurado. Cole a URL do Supabase."})

@app.route("/users", methods=["POST"])
def create_user():
    # DESCOMENTE QUANDO CONFIGURAR O POSTGRESQL
    # try:
    #     data = request.json
    #     cur = pg_conn.cursor()
    #     cur.execute(
    #         "INSERT INTO users (name, email, balance) VALUES (%s, %s, %s) RETURNING id, name, email",
    #         (data["name"], data["email"], data.get("balance", 0))
    #     )
    #     row = cur.fetchone()
    #     pg_conn.commit()
    #     cur.close()
    #     return jsonify({"status": f"✅ Usuário '{row[1]}' salvo no PostgreSQL!"})
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500
    return jsonify({"info": "⏳ PostgreSQL ainda não configurado. Cole a URL do Supabase."})

# ============================================================
# ROTAS - MONGODB (JOGOS) ⏳
@app.route("/games", methods=["GET"])
def get_games():
    try:
        if mongo_db is None:
            return jsonify({"error": "MongoDB não conectado"}), 500

        games = list(mongo_db.games.find({}, {"_id": 0}))
        return jsonify(games)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/games", methods=["POST"])
def create_game():
    try:
        if mongo_db is None:
            return jsonify({"error": "MongoDB não conectado"}), 500

        data = request.json

        title = data.get("title")
        genre = data.get("genre")

        if not title or not genre:
            return jsonify({"error": "Informe title e genre"}), 400

        game = {
            "title": title,
            "genre": genre
        }

        mongo_db.games.insert_one(game)

        return jsonify({"status": f"✅ Jogo '{title}' salvo no MongoDB!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# ===========================================================e a URL do Atlas."})

# ============================================================
# ROTAS - REDIS (RANKING) ⏳
# ============================================================

@app.route("/ranking", methods=["GET"])
def get_ranking():
    # DESCOMENTE QUANDO CONFIGURAR O REDIS
    # try:
    #     top = redis_client.zrevrange("leaderboard", 0, 9, withscores=True)
    #     ranking = [{"position": i+1, "username": u, "score": int(s)} for i, (u, s) in enumerate(top)]
    #     return jsonify(ranking)
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500
    return jsonify({"info": "⏳ Redis ainda não configurado. Cole a URL do Upstash."})

@app.route("/ranking", methods=["POST"])
def update_ranking():
    # DESCOMENTE QUANDO CONFIGURAR O REDIS
    # try:
    #     data = request.json
    #     redis_client.zadd("leaderboard", {data["username"]: data["score"]})
    #     return jsonify({"status": f"✅ Score de {data['username']} atualizado no Redis!"})
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500
    return jsonify({"info": "⏳ Redis ainda não configurado. Cole a URL do Upstash."})

# ============================================================
# START
# ============================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)