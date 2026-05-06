
# NetReplica - Guia de Configuração e Execução em Container

Este guia descreve os passos necessários para configurar e executar o NetReplica em um contêiner Docker, utilizando o Docker Compose. O NetReplica é uma ferramenta dedicada à automação de laboratórios de rede através de software.

## Pré-requisitos

- Docker instalado em sua máquina: <a target="_blank" href="https://docs.docker.com/get-docker/">Instruções de Instalação</a>
- Docker Compose instalado em sua máquina: <a target="_blank" href="https://docs.docker.com/compose/install/">Instruções de Instalação</a>

## Passo 1: Preparação do Ambiente

1. Abra um terminal e clone o repositório do NetReplica utilizando o seguinte comando:

```bash
git clone https://git.rnp.br/redes-abertas/netreplica-docker.git
```

2. Navegue para o diretório do NetReplica clonado:

```bash
cd netreplica-docker
```

## Passo 2: Inicialização do Contêiner

1. Para construir a imagem Docker e iniciar o contêiner NetReplica, execute:

```bash
docker compose up -d
```

Este comando criará e iniciará o contêiner em segundo plano.

## Passo 3: Utilização do NetReplica

Após a inicialização do contêiner, você pode interagir com o NetReplica utilizando os comandos abaixo.

### Execução do NetReplica

1. Coloque qualquer arquivo de configuração necessário (arquivos `.conf`) na pasta `conf` que está dentro do diretório `nrx` onde o repositório foi clonado.

2. Para executar o NetReplica com o arquivo `.conf`, utilize o seguinte comando:

```bash
docker exec -it nrx nrx -c conf/<arquivo.conf>
```

- Substitua `<arquivo.conf>` pelo nome do arquivo de configuração que você deseja utilizar.
- O diretório de saída para os resultados da execução já está especificado dentro do arquivo `.conf`, portanto, não é necessário especificá-lo no comando.

### Alias para Agilidade

Para otimizar ainda mais o uso do NetReplica, você pode criar um alias no seu shell para simplificar o comando de execução:

1. Abra um terminal e edite o arquivo de perfil do shell correspondente ao seu sistema (por exemplo, **`~/.bashrc`** para o Bash ou **`~/.zshrc`** para o Zsh).
2. Adicione a seguinte linha ao final do arquivo:

```bash
alias nrx='docker exec -it nrx nrx'
```

3. Salve o arquivo e feche-o.
4. Para ativar o novo alias sem reiniciar o terminal, execute o comando:

```bash
source ~/.bashrc   # ou source ~/.zshrc, dependendo do seu shell
```

Agora, você pode utilizar o comando simplificado **`nrx`** para executar o NetReplica de forma mais rápida. Por exemplo:

```bash
nrx -c conf/<arquivo.conf>
```

Agora para testar se o NetReplica está funcionando, execute o seguinte comando:

```bash
nrx -c conf/teste.conf
```

este comando ira fazer uma consulta no netbox de demonstração gerando um resultado igual o demonstrado abaixo:

```bash
--> nrx -c conf/teste.conf
Reading platform map from: templates/platform_map.yaml
Connecting to NetBox at: https://demo.netbox.dev
Fetching devices from sites: ['DM-Akron']
Created clab topology: conf/lab/lab.clab.yaml
To deploy this topology, run: sudo -E clab dep -t conf/lab/lab.clab.yaml
```

### Monitorando a Execução

- Durante a execução, o NetReplica usará as configurações do arquivo `.conf` para acessar o NetBox, iniciar a replicação e análise da rede. Monitore a saída do terminal para acompanhar o progresso e visualizar qualquer mensagem relevante.
- Após a conclusão da execução, os resultados da replicação e análise estarão disponíveis no diretório de saída especificado dentro do arquivo `.conf`.

### Encerrando o Contêiner

Para encerrar o contêiner NetReplica e liberar os recursos, execute:

```bash
docker compose down
```

## Próximos Passos: Configuração do Arquivo `.conf`

Agora que você já sabe como configurar e executar o NetReplica, 
o próximo passo é entender como configurar corretamente o arquivo `.conf` para atender às necessidades do seu ambiente de rede. 

proximos passos [Configuração do Arquivo `.conf`](NetReplica Guia Configuração e Execução com NetBox.md)

---

