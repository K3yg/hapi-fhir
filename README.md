# Teste técnico - Eduardo Brandt

## Arquitetura

O servidor FHIR escolhido foi o recomendado, no caso o HAPI FHIR.
Comecei lendo a [documentação disponível](https://hapifhir.io/hapi-fhir/docs/server_jpa/get_started.html) e então foi só seguir os passos apresentados para conseguir inicializar o servidor.

O arquivo docker-compose.yml está na pasta e contém todas as configurações necessárias, além de utilizar também o arquivo "hapi.application.yaml" para inserir configurações customizadas do servidor, por exemplo, a alteração de banco de dados.

Existe também o arquivo que está nesse caminho "..\src\main\resources\application.yaml" que vai conter algumas informações sobre a aplicação, entendi que não seria necessária nenhuma configuração diretamente nele, contudo, ainda sim é importante saber de sua existência.

### Banco de dados

Atualmente o uso do MySQL como alternativa de banco de dados para o servidor foi [depreciado](https://hapifhir.io/hapi-fhir/docs/server_jpa/database_support.html) em sua documentação, por não ter o desempenho satisfatório suficiente, então optei por usar o PostgreSQL.


### Inicialização

Para rodar o servidor, é necessário apenas utilizar o comando abaixo dentro da pasta "server" desse repositório.
```
docker compose up -d --build
```
Que irá realizar todas as instalações necessárias e deixará os serviços de pé e prontos para serem utilizados. 

É importante ressaltar que o processo de inicialização após executar o comando acima pode ser demorado.

O servidor estará rodando na porta [8080](localhost:8080).

#### Opção com Makefile

É importante ressaltar que o make deve estar instalado.
[Guia de instalação.](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows)

Após isso, é necessário apenas abrir o diretório do repositório mesmo, onde está localizado o arquivo Makefile e executar:
```
make run
```

## Carga de dados

Através do script Python, utilizando algumas bibliotecas para auxiliarem no tratamento dos dados, é possível:

* Criar pacientes no padrão RNDS
* Criar observação
* Formatar a data
* Mapear o gênero

Ao usar todas essas funções é possível garantir que os pacientes do arquivo CSV sejam cadastrados no banco de dados.

Também existe uma função a mais que exclui todos os pacientes e suas observações vinculadas para poder testar de forma mais fácil.

Para executar a carga de dados, é necessário apenas estar no diretório principal desse repositório e utilizar o comando:
```
python script.py
```
Ou caso tenha optado pela alterantiva do Makefile, também criei um comando para agilizar esse processo:
```
make load_data
```













