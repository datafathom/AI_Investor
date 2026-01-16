# Multi-stage build for React/Node/Socket.io Boilerplate
# Stage 1: Build the React app
FROM node:20-alpine AS builder
WORKDIR /app
# Install build dependencies for better-sqlite3
RUN apk add --no-cache python3 make g++
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production server
FROM node:20-alpine
WORKDIR /app
# Install build dependencies for better-sqlite3 (needed even in production)
RUN apk add --no-cache python3 make g++
COPY package*.json ./
RUN npm install --production
COPY --from=builder /app/dist ./dist
COPY server.js ./
# Copy config for any server-side configuration needs
COPY config/ ./config/
EXPOSE 3002
ENV NODE_ENV=production
ENV PORT=3002
CMD ["node", "server.js"]
