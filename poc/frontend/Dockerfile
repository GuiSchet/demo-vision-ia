FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY src/ ./src/
RUN npm run build
CMD ["npx","serve","-s","build","-l","3000"]
