# Imagem base com Python
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /src

# Copia arquivos do projeto para o container
COPY . .

# Instala as dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install black isort pylint pytest coverage bandit flake8

# Comando padrão (pode ser alterado para testes ou scripts)
CMD ["pytest"]
