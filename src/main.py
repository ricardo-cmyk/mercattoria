import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# Configurar CORS
CORS(app)

# Configurações do Supabase
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL e SUPABASE_KEY devem ser definidas nas variáveis de ambiente")

# Headers para requisições ao Supabase
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Rotas para lançamentos (perdas)
@app.route("/api/lancamentos", methods=["GET"])
def get_lancamentos():
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/lancamentos", headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erro ao carregar lançamentos do Supabase: {e}")
        return jsonify({
            "error": "Erro ao carregar lançamentos", 
            "details": str(e)
        }), 500
    except Exception as e:
        print(f"Erro inesperado ao carregar lançamentos: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route("/api/lancamentos", methods=["POST"])
def add_lancamento():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        # Validação básica
        required_fields = ['data', 'setor', 'filial', 'precoPerda', 'precoVenda']
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                return jsonify({"error": f"Campo obrigatório: {field}"}), 400
        
        # Validar tipos numéricos
        try:
            data['precoPerda'] = float(data['precoPerda'])
            data['precoVenda'] = float(data['precoVenda'])
        except (ValueError, TypeError):
            return jsonify({"error": "precoPerda e precoVenda devem ser valores numéricos"}), 400
        
        response = requests.post(f"{SUPABASE_URL}/rest/v1/lancamentos", headers=headers, json=data)
        response.raise_for_status()
        return jsonify(response.json()), 201
    except requests.exceptions.RequestException as e:
        print(f"Erro ao adicionar lançamento no Supabase: {e}")
        return jsonify({
            "error": "Erro ao adicionar lançamento", 
            "details": str(e)
        }), 500
    except Exception as e:
        print(f"Erro inesperado ao adicionar lançamento: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route("/api/lancamentos/<int:id>", methods=["PUT"])
def update_lancamento(id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        # Validar tipos numéricos se fornecidos
        if 'precoPerda' in data:
            try:
                data['precoPerda'] = float(data['precoPerda'])
            except (ValueError, TypeError):
                return jsonify({"error": "precoPerda deve ser um valor numérico"}), 400
        
        if 'precoVenda' in data:
            try:
                data['precoVenda'] = float(data['precoVenda'])
            except (ValueError, TypeError):
                return jsonify({"error": "precoVenda deve ser um valor numérico"}), 400
        
        response = requests.patch(f"{SUPABASE_URL}/rest/v1/lancamentos?id=eq.{id}", headers=headers, json=data)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erro ao atualizar lançamento no Supabase: {e}")
        return jsonify({
            "error": "Erro ao atualizar lançamento", 
            "details": str(e)
        }), 500
    except Exception as e:
        print(f"Erro inesperado ao atualizar lançamento: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route("/api/lancamentos/<int:id>", methods=["DELETE"])
def delete_lancamento(id):
    try:
        response = requests.delete(f"{SUPABASE_URL}/rest/v1/lancamentos?id=eq.{id}", headers=headers)
        response.raise_for_status()
        return jsonify({"message": "Lançamento excluído com sucesso"})
    except requests.exceptions.RequestException as e:
        print(f"Erro ao deletar lançamento no Supabase: {e}")
        return jsonify({
            "error": "Erro ao deletar lançamento", 
            "details": str(e)
        }), 500
    except Exception as e:
        print(f"Erro inesperado ao deletar lançamento: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

# Rotas para filiais
@app.route("/api/filiais", methods=["GET"])
def get_filiais():
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/filiais", headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erro ao carregar filiais do Supabase: {e}")
        return jsonify({
            "error": "Erro ao carregar filiais", 
            "details": str(e)
        }), 500
    except Exception as e:
        print(f"Erro inesperado ao carregar filiais: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route("/api/filiais", methods=["POST"])
def add_filial():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        # Validação básica
        if 'nome' not in data or not data['nome']:
            return jsonify({"error": "Campo obrigatório: nome"}), 400
        
        response = requests.post(f"{SUPABASE_URL}/rest/v1/filiais", headers=headers, json=data)
        response.raise_for_status()
        return jsonify(response.json()), 201
    except requests.exceptions.RequestException as e:
        print(f"Erro ao adicionar filial no Supabase: {e}")
        return jsonify({
            "error": "Erro ao adicionar filial", 
            "details": str(e)
        }), 500
    except Exception as e:
        print(f"Erro inesperado ao adicionar filial: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route("/api/filiais/<int:id>", methods=["PUT"])
def update_filial(id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        response = requests.patch(f"{SUPABASE_URL}/rest/v1/filiais?id=eq.{id}", headers=headers, json=data)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erro ao atualizar filial no Supabase: {e}")
        return jsonify({
            "error": "Erro ao atualizar filial", 
            "details": str(e)
        }), 500
    except Exception as e:
        print(f"Erro inesperado ao atualizar filial: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route("/api/filiais/<int:id>", methods=["DELETE"])
def delete_filial(id):
    try:
        response = requests.delete(f"{SUPABASE_URL}/rest/v1/filiais?id=eq.{id}", headers=headers)
        response.raise_for_status()
        return jsonify({"message": "Filial excluída com sucesso"})
    except requests.exceptions.RequestException as e:
        print(f"Erro ao deletar filial no Supabase: {e}")
        return jsonify({
            "error": "Erro ao deletar filial", 
            "details": str(e)
        }), 500
    except Exception as e:
        print(f"Erro inesperado ao deletar filial: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

# Rota de health check
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "BI Perdas API está funcionando"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

