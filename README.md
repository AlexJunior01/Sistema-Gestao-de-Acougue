# Sistema de Gestão de Açougue

## Como executar
1- Baixe o projeto do GitHub no seguinte link: https://github.com/AlexJunior01/Sistema-Gestao-de-Acougue .

2- Entre na pasta principal do projeto, e a partir dela vamos fazer a instalação de um ambiente virtual, para que não haja conflitos de bibliotecas no computador (Esse passo é opcional, caso não queira segui-lo pule para o passo 5).

3- Siga o tutorial do link a seguir para fazer a instalação do ambiente virtual. Quando chegar no passo "Create an Environment in Linux and MacOS" certifique-se de estar dentro da pasta principal do projeto. 
https://phoenixnap.com/kb/install-flask .

4- Ative o ambiente virtual e faça a instalação dos requisitos utilizando nosso arquivo requirements.txt com o comando

```bash
pip install -e .
```

5- Faça a instalação do SQLITE3 em seu computador seguindo o tutorial do link a seguir: https://www.tutorialspoint.com/sqlite/sqlite_installation.htm .

6- Execute o seguinte script para fazer a criação das tabelas.

```bash
flask init-db
```

7- Entre novamente no ambiente virtual e execute o arquivo "__init__.py" para executar o Flask.

```bash
flask run
```

8- Acesse a pagina principal do projeto a partir de: http://localhost:5000/ 
