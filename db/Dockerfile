# Use the official Redis image as the base
FROM redis:latest

# Optional: Set a working directory (where the commands within the container are executed)
WORKDIR /data

# Expose the default Redis port
EXPOSE 6379

# Specify the command to start the Redis server (this is inherited from the base image)
CMD [ "redis-server" ] 