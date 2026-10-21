from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# ==========================================
# BASE DE DADOS FISCAL (Exercícios)
# ==========================================
produtos_fiscais = {
    "1": {"preco": 2500.0, "categoria": "Laptops"},
    "2": {"preco": 1200.0, "categoria": "Monitores"}
}

produtos_comerciais = {}
produtos_tecnicos = {}

# ==========================================
# EXEMPLO DA AULA
# ==========================================
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({
        "mensagem": "Olá do Flask!",
        "status": "success",
        "tecnologia": "Python"
    })

# ==========================================
# EXERCÍCIO 1: Detalhes Fiscais
# ==========================================
@app.route('/detalhes/<id>', methods=['GET'])
def detalhes(id):
    if id in produtos_fiscais:
        return jsonify(produtos_fiscais[id])
    return jsonify({"error": "NOT_FOUND"}), 404

# ==========================================
# EXERCÍCIO 3: Status do Serviço
# ==========================================
@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "service": "Flask",
        "status": "online",
        "timestamp": datetime.now().isoformat()
    })

# ==========================================
# EXERCÍCIO 4: Cadastro Fiscal (POST)
# ==========================================
@app.route('/fiscal/cadastrar', methods=['POST'])
def cadastrar_fiscal():
    dados = request.get_json()
    id_prod = dados.get('id')
    preco_base = dados.get('preco_base')
    categoria = dados.get('categoria')
    
    # Cálculo fiscal: 20% de imposto
    preco_calculado = preco_base * 1.20
    
    # Persistência
    produtos_tecnicos[id_prod] = {
        "preco": preco_calculado,
        "categoria": categoria
    }
    
    produtos_fiscais[id_prod] = {
        "preco": preco_calculado,
        "categoria": categoria
    }
    
    print(f"[FLASK] Cadastrado ID {id_prod}: preco={preco_calculado}")
    return jsonify({"status": "created"}), 201

# ==========================================
# EXERCÍCIO 5: Validação de ID
# ==========================================
@app.route('/fiscal/<id>', methods=['GET'])
def fiscal_validado(id):
    try:
        id_int = int(id)
        if id_int <= 0:
            raise ValueError
    except ValueError:
        return jsonify({
            "error": "INVALID_ID",
            "message": "O ID deve ser um inteiro positivo"
        }), 400
    
    if id in produtos_fiscais:
        return jsonify(produtos_fiscais[id])
    return jsonify({"error": "NOT_FOUND"}), 404

# ==========================================
# EXECUÇÃO
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
