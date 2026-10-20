const express = require('express');
const app = express();
app.use(express.json());

const PORT = 3000;
const locks = new Set(); // Memória dos locks ativos

// POST /lock - Adquirir lock
app.post('/lock', (req, res) => {
    const { resource } = req.body;
    console.log(`Recebido pedido de lock para o recurso ${resource}`);
    
    if (locks.has(resource)) {
        console.log(`Recurso ${resource} já está em uso, negando lock.`);
        return res.status(409).json({ message: "Conflict", acquired: false });
    }
    
    locks.add(resource);
    console.log(`Lock concedido para o recurso ${resource}`);
    res.status(200).json({ message: "OK", acquired: true });
});

// POST /unlock - Liberar lock
app.post('/unlock', (req, res) => {
    const { resource } = req.body;
    if (locks.has(resource)) {
        locks.delete(resource);
        console.log(`Lock para o recurso ${resource} liberado.`);
    }
    res.status(200).json({ message: "Unlocked" });
});

app.listen(PORT, () => {
    console.log(`Serviço Coordenador rodando na porta ${PORT}`);
});
