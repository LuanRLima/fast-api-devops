INSERT INTO employees (first_name, last_name, department, email)
VALUES ('John', 'Doe', 'IT', 'johndoe@mail.com'), ('Bill', 'Campbell', 'HR', 'billcampbell@mail.com');

Dockerfile
Agora, para usar esses scripts numa imagem do Docker, vamos criar um Dockerfile com a seguinte implementação:

# Derivando da imagem oficial do MySQL
FROM mysql:5.7

# Adicionando um database (variável de ambiente)
ENV MYSQL_DATABASE Company

# Adicionando os scripts SQL para serem executados na criação do banco
COPY ./database/ /docker-entrypoint-initdb.d/
Imagem do Docker
Para criar uma imagem baseada nesse Dockerfile, na pasta MYSQL, basta executar o seguinte comando:

docker build -t company-database .
E conferir depois se a imagem foi gerada através do comando:

docker images

Com o retorno:

REPOSITORY            TAG        IMAGE ID             CREATED           SIZE
company-database     latest    89b38d78dc16        20 seconds ago       431MB
Testando o Container
Para iniciar um container baseado nessa imagem, podemos agora seguir com o comando:

docker run -d -p 3306:3306 --name company-database -e
MYSQL_ROOT_PASSWORD=RootPassword company-database
Observação: a flag -e permite informar variáveis de ambiente. Aqui, apenas foi usado para configurar a senha do banco: MYSQL_ROOT_PASSWORD (daria também para definir aqui o database, mas já fizemos isso no Dockerfile com a variável MYSQL_DATABASE).

Será possível consultar que o container está UP usando o comando:

docker ps
Poderemos, a partir desse momento, acessar nosso banco através do Docker usando:

docker exec -it company-database bash
E conectar nele com:

mysql -uroot -p

Enter password: (RootPassword)
Observação: lembrando que você pode rodar o comando exit em qualquer momento para sair do mysql ou do container do Docker.

A partir desse momento, já poderemos realizar operações mysql.

1. Para ver o Database, podemos executar o comando:

mysql> show databases;
Com o retorno:

+--------------------+
| Database           |
+--------------------+
| information_schema |
| Company            |
| mysql              |
| performance_schema |
| sys                |
+--------------------+

2. Para usar o nosso database Company, execute o comando:

mysql> use Company;
As tabelas de nosso database Company podem ser listadas usando o comando:

mysql> show tables;
Com o retorno:

+-------------------+
| Tables_in_company |
+-------------------+
| employees         |
+-------------------+
3. As colunas dessa tabela employees podem ser listadas executando o comando:

mysql> show columns from employees;
Com o retorno:

+------------+-------------+------+-----+---------+-------+
| Field      | Type        | Null | Key | Default | Extra |
+------------+-------------+------+-----+---------+-------+
| first_name | varchar(25) | YES  |     | NULL    |       |
| last_name  | varchar(25) | YES  |     | NULL    |       |
| department | varchar(15) | YES  |     | NULL    |       |
| email      | varchar(50) | YES  |     | NULL    |       |
+---+------+-----+---------+------+-----+---------+-------+
4. O conteúdo da tabela employees pode ser observado através do comando:

mysql> select * from employees;
Com o retorno:

+------------+-----------+------------+-----------------------+
| first_name | last_name | department | email                 |
+------------+-----------+------------+-----------------------+
| John       | Doe       | IT         | johndoe@mail.com      |
| Bill       | Campbell  | HR         | billcampbell@mail.com |
+------------+-----------+------------+-----------------------+
Pronto! Temos nossa imagem personalizada do Docker de um banco de dados MySQL!

Esta imagem do Docker seria uma ótima solução para compartilhar e garantir que várias pessoas desenvolvedoras usem as mesmas configurações num ambiente de desenvolvimento local, apenas iniciando um container a partir da imagem.

Lembrando que para desmontá-lo, é só seguir o mesmo passo a passo da parte anterior.

Pontos de atenção
É importante notar, no entanto, que essa nem sempre é a melhor solução! Por exemplo:

Caso insira muitos dados, o tamanho da sua imagem aumentará significativamente;
Quando quiser atualizar os dados, é preciso construir uma nova imagem.
Back end + MYSQL
Agora entramos na parte legal!

Aqui, o código da API Rest em Python usava hardcoded nas configurações do banco de dados, configurados ao subir meu container company-database.

Ressalva: não faça isso em PROD, hein? Use arquivos de configurações para cada ambiente, aqui foi apenas para exemplificar!

Seguindo esse passo a passo, você já percebeu que quando trabalhamos com vários containers, gerenciar a execução deles pode se tornar mais complexo.

Por exemplo: imagine se eu tivesse cinco ou mais containers para cuidar ao mesmo tempo na minha máquina local, toda vez que eu precisar fazer um teste…

Felizmente, para isso, temos algumas tecnologias que auxiliam, sendo uma delas o Docker Compose.

Docker Compose
Para usar o Docker Compose, basta criar um arquivo docker-compose.yml na raiz do projeto, sendo agora a estrutura do nosso projeto a seguinte:

docker-mysql-python
    |__ backend
    |__ database
    |__ docker-compose.yml

O conteúdo desse arquivo seria:

version: '3.5'
services:
    backend:
        image: company-backend
        ports:
            - "80:80"
    mysql:
        image: company-database
        ports:
            - "3306:3306"
        environment:
            MYSQL_ROOT_PASSWORD: RootPassword
            MYSQL_DATABASE: Company
Como podem observar, as configurações usam as nossas duas imagens locais (que podemos conferir usando o comando docker images) com portas e variáveis de ambiente pré-configuradas (conforme era feito previamente nos comandos docker run).

Após ter desmontado os containers das seções anteriores (para evitar conflitos entre nomes de containers), na pasta root do repositório, execute o comando:

docker-compose up
O funcionamento deve ser igual ao de subir os containers separadamente na mão. A vantagem é que usando o Docker Compose, os containers são configurados e são desmontados em conjunto de maneira mais simples.

Vamos conferir abrindo o navegador, daria para acessar a página inicial do aplicativo na URL http://0.0.0.0/ retornando novamente o texto Hello World.

Também daria agora para acessar a URL http://0.0.0.0/employees com sucesso, que retornaria a lista de empregados presentes no banco.

Pronto! Conferimos que com apenas um comando, conseguimos subir vários containers em conjunto.

Para sair do prompt do docker-compose up, use as teclas CTRL + C.

Isso não vai remover os containers, será ainda possível ver eles usando o comando docker ps -a.

Para desmontar os containers, use o seguinte comando:

docker-compose down
Executando o comando docker ps -a agora, os containers não deveriam mais aparecer.

Conclusão
Neste artigo, detalhamos como configurar uma API Rest em Python com um banco de dados MYSQL usando FastAPI, assim como usar imagens do Docker para personalizar um banco de dados MySQL.

Observamos também que gerenciar vários containers ao mesmo tempo pode ser trabalhoso e que usar o Docker Compose pode agilizar muito esse processo.

Lembrando que o código-fonte desse projeto pode ser encontrado no GitHub.

Se quiser aprofundar o uso do Docker, sugiro também a leitura destes dois excelentes livros gratuitos no GitHub: do badtuxx (aka Jeferson do LINUXtips) e do gomex (aka Rafael Gomes).

Ficou com alguma dúvida sobre esse tutorial de Docker na prática? Então deixe um comentário!

Referências
Customize your MySQL Database in Docker
Docker Compose
Docs Docker
FastAPI in Containers

