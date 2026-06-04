FROM node:20-alpine

# Criação de usuário não-privilegiado (Zero Trust - Workload)
RUN addgroup -S lexgrid && adduser -S lexgrid -G lexgrid

WORKDIR /app

# Copia apenas os arquivos de dependência primeiro (Aproveita o cache do Docker)
COPY package*.json ./
RUN npm install

COPY . .

# Ajusta permissões e troca para o usuário restrito
RUN chown -R lexgrid:lexgrid /app

USER lexgrid

EXPOSE 3000
CMD ["npm", "run", "dev"]