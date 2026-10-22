FROM node:18-alpine

WORKDIR /app

# Copia o package.json e instala dependências
COPY package*.json ./
RUN npm install

# Copia o código
COPY . .

# Expõe a porta
EXPOSE 3000

# Comando de execução
CMD ["node", "server.js"]
