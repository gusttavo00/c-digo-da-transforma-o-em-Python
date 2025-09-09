import uuid
import sqlite3
from flask import Flask, jsonify, render_template
from flask.views import MethodView
from flask_smorest import Blueprint, Api, abort
from marshmallow import Schema, fields

# --- Configuração do Banco de Dados ---
DB_NAME = "database.db"

def init_db():
    """Cria a tabela de usuários, se ela não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# --- Configuração da Aplicação Flask e Swagger ---
app = Flask(__name__)
app.config["API_TITLE"] = "API de Gerenciamento de Usuários"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
blp = Blueprint("usuarios", __name__, url_prefix="/api/usuarios", description="Operações sobre usuários")

# --- Schemas de Validação (Marshmallow) ---
class UsuarioSchema(Schema):
    id = fields.Str(dump_only=True)
    nome = fields.Str(required=True, error_messages={"required": "O nome é obrigatório."})
    email = fields.Str(required=True, error_messages={"required": "O e-mail é obrigatório."})

class UsuarioUpdateSchema(Schema):
    nome = fields.Str()
    email = fields.Str()

# --- Endpoints da API ---
@blp.route("/")
class Usuarios(MethodView):
    """Recurso para lidar com a lista de usuários."""

    @blp.response(200, UsuarioSchema(many=True))
    def get(self):
        """Retorna a lista de todos os usuários."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()
        
        # Converte a lista de tuplas em uma lista de dicionários
        return [{"id": u[0], "nome": u[1], "email": u[2]} for u in usuarios]

    @blp.arguments(UsuarioSchema)
    @blp.response(201, UsuarioSchema)
    def post(self, novo_usuario):
        """Cria um novo usuário."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        try:
            novo_usuario_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO usuarios (id, nome, email) VALUES (?, ?, ?)", 
                           (novo_usuario_id, novo_usuario["nome"], novo_usuario["email"]))
            conn.commit()
            novo_usuario["id"] = novo_usuario_id
            return novo_usuario
        except sqlite3.IntegrityError:
            abort(409, message="Um usuário com este e-mail já existe.")
        finally:
            conn.close()

@blp.route("/<string:usuario_id>")
class Usuario(MethodView):
    """Recurso para lidar com um único usuário por ID."""

    @blp.response(200, UsuarioSchema)
    def get(self, usuario_id):
        """Retorna os dados de um usuário específico."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id=?", (usuario_id,))
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario is None:
            abort(404, message="Usuário não encontrado.")
        
        return {"id": usuario[0], "nome": usuario[1], "email": usuario[2]}

    @blp.arguments(UsuarioUpdateSchema)
    @blp.response(200, UsuarioSchema)
    def put(self, dados_atualizados, usuario_id):
        """Atualiza os dados de um usuário."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM usuarios WHERE id=?", (usuario_id,))
            usuario_existente = cursor.fetchone()
            if not usuario_existente:
                abort(404, message="Usuário não encontrado.")

            nome_novo = dados_atualizados.get("nome", usuario_existente[1])
            email_novo = dados_atualizados.get("email", usuario_existente[2])

            cursor.execute("UPDATE usuarios SET nome=?, email=? WHERE id=?", 
                           (nome_novo, email_novo, usuario_id))
            conn.commit()
            
            return {"id": usuario_id, "nome": nome_novo, "email": email_novo}
        except sqlite3.IntegrityError:
            abort(409, message="O e-mail fornecido já está em uso por outro usuário.")
        finally:
            conn.close()

    @blp.response(204)
    def delete(self, usuario_id):
        """Exclui um usuário."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (usuario_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            abort(404, message="Usuário não encontrado.")
        
        conn.close()
        return {} # Retorno vazio para 204

# --- Rota para a página HTML (Frontend) ---
@app.route("/")
def home():
    """Renderiza o HTML para a interface do usuário."""
    return render_template("index.html")

# --- Registro do Blueprint e Inicialização ---
api.register_blueprint(blp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)