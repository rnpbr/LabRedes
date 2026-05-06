# Primeiros Passos: Preparando o Ambiente

## :octicons-book-24: **1. Introdução**

Neste guia, abordaremos os primeiros passos para preparar o ambiente de monitoramento usando a rede Docker br-lab. 
Esta rede foi criada para facilitar o acesso, monitoramento e uso de ferramentas de análise nos laboratórios gerenciados pelo Containerlab. 
A configuração da rede br-lab é um passo necessário para a utilização da maioria das ferramentas que serão mostradas neste guia. 
Após a configuração das ferramentas de monitoramento na rede br-lab, elas poderão ser utilizadas em qualquer laboratório, 
eliminando a necessidade de reconfiguração a cada novo ambiente. Isso simplifica os testes de múltiplas configurações 
e permite a utilização de diversas ferramentas de análise com maior eficiência.

### :material-checkbox-marked-outline: **Vantagens:**

- **Configuração única**: As ferramentas de monitoramento só precisam ser configuradas uma vez, independentemente do laboratório em uso.
- **Facilidade nos testes**: Possibilita a criação e teste de várias configurações laboratoriais sem a necessidade de ajustes contínuos nas ferramentas.
- **Integração flexível**: Permite adicionar facilmente novos laboratórios e dispositivos à rede sem impactos na infraestrutura já configurada.

---

### :octicons-graph-24: **Exemplos de Laboratórios que Utilizam a Rede br-lab**

---

### :fontawesome-solid-diagram-project: **Diagrama da Rede de Monitoramento**

Abaixo está um exemplo visual que mostra como a rede de monitoramento `br-lab` está configurada, conectando diferentes laboratórios e dispositivos para um ambiente de testes unificado e eficiente.
![br-lab_diagram.svg](../../img/tools_imgs/br-lab_diagram.svg)
---

## :material-tools:  **2. Criando a Rede Docker**

### :octicons-terminal-24: **Comando para Criar a Rede:**

```bash
docker network create \
  --driver=bridge \
  --opt com.docker.network.bridge.name=br-lab \
  --subnet=172.10.10.0/24 \
  br-lab

```

### :gear: **Explicação dos Parâmetros:**

- `docker network create`: Inicia a criação de uma nova rede Docker.
- `-driver=bridge`: Especifica o driver da rede (bridge).
- `-opt com.docker.network.bridge.name=br-lab`: Define o nome da interface de rede bridge no host.
- `-subnet=172.10.10.0/24`: Define a sub-rede (até 254 IPs disponíveis).
- `br-lab`: Nome da rede.

## :octicons-diff-added-24: **3. Adicionando Containers à Rede**

### :material-docker: **Usando Docker Run:**

Comando para adicionar um container à rede:

```bash
docker run -d \
  --name meu_container \
  --network br-lab \
  imagem_do_container

```

### :gear: **Explicação dos Parâmetros:**

- `docker run -d`: Executa o container em segundo plano.
- `-name meu_container`: Nome do container.
- `-network br-lab`: Conecta o container à rede `br-lab`.
- `imagem_do_container`: Especifica a imagem do container a ser utilizada.

### :material-docker: **Usando Docker Compose:**

Se a rede já foi criada, use o Docker Compose para configurar containers com IPs estáticos.

```yaml
version: '3.8'

networks:
  br-lab:
    external: true

services:
  meu_container:
    image: imagem_do_container
    networks:
      br-lab:
        ipv4_address: 172.10.10.101 # opcicional para ip estatico

```

!!! warning "Atenção"
    Ao ultilizar ips estaticos, certifique-se de ultilizar ips apos `172.10.10.100`, afim de evitar conflitos com os containers existentes.

### :gear: **Explicação da Configuração:**

- `networks`: Define as redes que os serviços usarão.
- `br-lab`: Indica que a rede já foi criada externamente (external: true).
- `services`: Define os containers a serem executados.
- `ipv4_address`: Atribui um IP estático ao container (recomendado utilizar endereços após `172.10.10.100`).

## :material-help-network: **4. Funcionamento da Rede**

A rede `br-lab` usa o driver `bridge`, o que permite comunicação interna entre os containers, mantendo-os isolados do sistema host. Isso oferece:

- **Isolamento**: Os containers não interferem em outros processos do host.
- **Comunicação interna**: Containers podem se comunicar usando IPs na sub-rede especificada.

## :material-connection: **5. Conectando Roteadores com Cabos Virtuais**

Para conectar roteadores na rede `br-lab` usando cabos virtuais via Containerlab, você pode configurar as conexões entre interfaces.

### :gear: **Exemplo de Conexões:**

```yaml
br-lab:
  kind: bridge

links:
  - endpoints: ["route1:eth1", "br-lab:eth1"]
  - endpoints: ["route2:eth1", "br-lab:eth2"]
  - endpoints: ["route3:eth1", "br-lab:eth3"]
  - endpoints: ["route4:eth1", "br-lab:eth4"]

```

### :material-lan-connect: **Explicação das Conexões:**

- Cada linha define um “cabo virtual” conectando duas interfaces de rede (por exemplo, `route1:eth1` está conectado a `br-lab:eth1`).
- Isso permite a comunicação entre dispositivos (roteadores e ferramentas de monitoramento) através dessas interfaces.

## :material-file-document-check: **6. Conclusão**

Com este guia, você aprendeu a criar e utilizar a rede Docker `br-lab`, a adicionar containers à rede e a conectar roteadores virtualmente. Essa configuração é ideal para monitoramento eficiente em ambientes de laboratório.

---