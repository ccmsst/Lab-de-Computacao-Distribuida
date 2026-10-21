const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3000;

app.use(express.json());

// ==========================================
// BASE DE DADOS ESTOQUE
// ==========================================
const produtos_estoque = {
    "1": {"nome": "Dell XPS 13", "estoque": 10},
    "2": {"nome": "Monitor LG 29", "estoque": 5}
};

// ==========================================
// EXEMPLO DA AULA
// ==========================================
app.get('/api/data', (req, res) => {
    res.json({
        "mensagem": "Olá do Node.js!",
        "status": "sucesso",
        "tecnologia": "JavaScript"
    });
});

// ==========================================
// EXERCÍCIO 1 + 5: Detalhes de Estoque (COM VALIDAÇÃO)
// ==========================================
app.get('/estoque/:id', (req, res) => {
    const id = req.params.id;
    
    // VALIDAÇÃO (Exercício 5)
    const id_int = parseInt(id);
    if (isNaN(id_int) || id_int <= 0 || String(id_int) !== id) {
        return res.status(400).json({
            "error": "INVALID_ID",
            "message": "O ID deve ser um inteiro positivo"
        });
    }
    
    // Buscar no estoque
    if (produtos_estoque[id]) {
        res.json(produtos_estoque[id]);
    } else {
        res.status(404).json({"error": "NOT_FOUND"});
    }
});

// ==========================================
// EXERCÍCIO 2: Server-to-Server (Proxy)
// ==========================================
app.get('/api/full-info/:id', async (req, res) => {
    const id = req.params.id;
    
    // Validação
    const id_int = parseInt(id);
    if (isNaN(id_int) || id_int <= 0) {
        return res.status(400).json({
            "error": "INVALID_ID",
            "message": "O ID deve ser um inteiro positivo"
        });
    }
    
    try {
        const response = await axios.get(`http://localhost:5000/detalhes/${id}`);
        const fiscal = response.data;
        const estoque = produtos_estoque[id] || {};
        
        res.json({
            id: id,
            nome: estoque.nome,
            preco: fiscal.preco,
            categoria: fiscal.categoria,
            estoque: estoque.estoque
        });
    } catch (error) {
        res.status(404).json({"error": "NOT_FOUND"});
    }
});

// ==========================================
// EXERCÍCIO 3: Status
// ==========================================
app.get('/status', (req, res) => {
    res.json({
        "service": "Node",
        "status": "online",
        "timestamp": new Date().toISOString()
    });
});

// ==========================================
// EXERCÍCIO 4: Cadastro Completo
// ==========================================
app.post('/cadastrar', async (req, res) => {
    const { id, nome, estoque, preco_base, categoria } = req.body;
    
    const nome_maiusculo = nome.toUpperCase();
    
    produtos_estoque[id] = {
        "nome": nome_maiusculo,
        "estoque": estoque
    };
    
    try {
        await axios.post('http://localhost:5000/fiscal/cadastrar', {
            id: id,
            preco_base: preco_base,
            categoria: categoria
        });
        console.log(`[NODE] Sincronizado com Flask: ID ${id}`);
    } catch (error) {
        console.log("Erro ao sincronizar com Flask:", error.message);
    }
    
    res.status(201).json({
        "status": "created",
        "id": id,
        "nome": nome_maiusculo,
        "estoque": estoque
    });
});

// ==========================================
// EXECUÇÃO
// ==========================================
app.listen(PORT, () => {
    console.log(`Servidor Node rodando na porta ${PORT}`);
});