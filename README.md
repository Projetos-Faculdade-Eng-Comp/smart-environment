# Smart Environment

Trabalho 02 da disciplina de Sistemas Distribuídos do curso de Engenharia de Computação 2023.2

## Conceito

## Tecnologias utilizadas:

### Linguagens:

- Python

### Frameworks:

- **RabbitMQ:**
- **gRPC:**

## Instalação

Primeiro, certifique-se que a sua máquina possui o Docker instalado, pois tal ferramenta é necessária para a execução do servidor RabbitMQ. Além disso, garanta que o gerenciador de pacotes `pip` esteja instalado e atualizado.

```bash
$ python3 -m pip install --upgrade pip
```

Então, realize um `git clone` deste repositório e crie um ambiente virtual Python com os seguintes comandos:

```bash
$ python3 -m venv venv # Criar o ambiente virtual chamado venv
$ souce venv/bin/activate # Ativar o ambiente virtual
```

Agora, com o ambiente virtual ativo, instale as dependências dos frameworks:

```bash
$ python3 -m pip install pika --upgrade # Biblioteca para usar o RabbitMQ
$ python3 -m pip install grpcio # Biblioteca para usar o gRPC
$ python3 -m pip install grpcio-tools # Pacote com ferramentas como protobuf
```

Por fim, com o Docker executando, utilizar o seguinte comando para iniciar o servidor padrão do RabbitMQ:

```bash
$ docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```

Desta forma, basta executar o arquivo `.py` desejado.
