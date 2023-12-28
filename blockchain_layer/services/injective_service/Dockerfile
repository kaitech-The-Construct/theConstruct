# Use the official lightweight Node.js 18 image.
# https://hub.docker.com/_/node
FROM node:18-alpine

# Create and change to the app directory.
WORKDIR /usr/src/app

# Copy all project files to the container
# Files in the location of this file are copied to WORKDIR in the container
COPY . .

RUN apk add --update python3 make g++\
   && rm -rf /var/cache/apk/*

# Makes sure npm is up to date otherwise install dependencies attempts will fail
RUN yarn global add yarn

# Install dependencies
RUN yarn install

# The process this container should run
CMD ["node", "start"]
