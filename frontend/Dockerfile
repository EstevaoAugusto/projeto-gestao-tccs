# Imagem oficial do Node.js compativel com os requisitos do Vite.
FROM node:22-alpine

# Diretório de trabalho dentro do container.
WORKDIR /app

# Copia apenas os manifests primeiro para aproveitar cache de dependencias.
COPY package*.json ./

# Instala dependencias do projeto Vue.js.
RUN npm install

# Copia o restante do codigo-fonte.
COPY . .

# Porta usada pelo Vite.
EXPOSE 5173

# Comando padrao; o docker-compose sobrescreve mantendo os mesmos parametros.
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
