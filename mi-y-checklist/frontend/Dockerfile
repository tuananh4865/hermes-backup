FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install --no-audit --no-fund

# Copy source
COPY . .

# Build
RUN npm run build

EXPOSE 3000

CMD ["npx", "next", "start", "-p", "3000"]
