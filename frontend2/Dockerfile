FROM node:18-alpine

WORKDIR /app

# Copy package files first (for caching)
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy the rest of the frontend code
COPY . .

# Build arguments for environment variables
ARG VITE_BACKEND_PORT=5000
ENV VITE_BACKEND_PORT=$VITE_BACKEND_PORT

EXPOSE 5173

# Start development server with host binding
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
