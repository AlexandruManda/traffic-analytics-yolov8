FROM node:18 AS builder

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

# Build the frontend application
RUN npm run build

# Use Nginx as the final image
FROM nginx:latest

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the built frontend files to Nginx
COPY --from=builder /app/build /usr/share/nginx/html

# Copy the custom Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 for HTTP and 443 for HTTPS (if needed)
EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]