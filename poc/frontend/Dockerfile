FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
COPY vite.config.js ./
RUN npm install
COPY src/ ./src/
RUN npm run build
CMD ["npm", "start"]
