FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD password
ENV MYSQL_DATABASE your_database_name
ENV MYSQL_USER your_database_user
ENV MYSQL_PASSWORD your_database_user_password

RUN set -x && \
    echo "Creating database: ${MYSQL_DATABASE}" && \
    mysql -u root -proot -e "CREATE DATABASE ${MYSQL_DATABASE};" && \
    echo "Creating user: ${MYSQL_USER}" && \
    mysql -u root -proot -e "CREATE USER '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';" && \
    echo "Granting privileges to user: ${MYSQL_USER}" && \
    mysql -u root -proot -e "GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'localhost';" && \
    echo "Flushing privileges" && \
    FLUSH PRIVILEGES;