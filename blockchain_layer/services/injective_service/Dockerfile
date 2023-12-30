# Use the official lightweight Node.js 18 image.
# https://hub.docker.com/_/node
FROM node:20-bookworm-slim

# Create and change to the app directory.
WORKDIR /

# Copy application dependency manifests to the container image.
# A wildcard is used to ensure both package.json AND package-lock.json are copied.
# Copying this separately prevents re-running npm install on every code change.
COPY package*.json ./
COPY ./yarn.lock ./
# Install dependencies.
# RUN apk add --update python3 make g++\
#    && rm -rf /var/cache/apk/*
# If you add a package-lock.json speed your build by switching to 'npm ci'.
RUN yarn install


# Copy local code to the container image.
COPY . ./

# Run the web service on container startup.
CMD ["node", "dist/index.js"]

