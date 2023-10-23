# Step 1: Build the Node.js app
FROM node:18 as build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY ./web-tts/package*.json .

# Install app dependencies
RUN npm install

COPY ./web-tts/. .

# Build the Node.js app
RUN npm run build-only

# Step 2: Create the Nginx server
FROM nginx:alpine

# Copy the built Node.js app from the previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose the port for Nginx
EXPOSE 80
EXPOSE 443

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
