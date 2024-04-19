FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD password
ENV MYSQL_DATABASE my_database
ENV MYSQL_USER my_user
ENV MYSQL_PASSWORD my_password

RUN set -x && \
    while ! mysqladmin ping -h"localhost" --silent; do sleep 1; done && \
    # Database and User Setup (within the RUN instruction)
    echo "Creating database: ${MYSQL_DATABASE}" && \
    mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};" && \
    echo "Creating user: ${MYSQL_USER}" && \
    mysql -u root -proot -e "CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';" && \
    echo "Granting privileges to user: ${MYSQL_USER}" && \
    mysql -u root -proot -e "GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'localhost';" && \
    echo "Flushing privileges" && \
    FLUSH PRIVILEGES;

# Non-root User for improved security
RUN useradd -ms /bin/bash mysql_user

# Set Working Directory for script location
WORKDIR /docker-entrypoint-initdb.d

# Ensure correct ownership for the copied script
RUN chown -R mysql_user:mysql_user .

# Switch to our less-privileged user and start MySQL
USER mysql_user
CMD ["mysqld"]