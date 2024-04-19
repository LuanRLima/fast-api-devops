FROM mysql:5.7

# Adicionando um database (variável de ambiente)
ENV MYSQL_DATABASE Company
ENV MYSQL_ROOT_PASSWORD=123456
ENV MYSQL_USER=my_user
ENV MYSQL_PASSWORD=my_password

# Adicionando os scripts SQL para serem executados na criação do banco
COPY ./employees.sql/ /docker-entrypoint-initdb.d/