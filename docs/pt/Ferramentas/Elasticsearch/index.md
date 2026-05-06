# Guia de Instalação do ELK (Elasticsearch)

## :octicons-book-24: 1. Introdução

Neste guia, abordaremos a configuração do stack **ELK** (Elasticsearch, Logstash e Kibana) para monitoramento e 
análise de dados em ambientes laboratoriais. O ELK é uma poderosa combinação de ferramentas que permite a coleta, 
armazenamento, análise e visualização de dados em tempo real, sendo amplamente utilizado para gerenciamento de logs e 
monitoramento de sistemas.

## :simple-elastic: 2. O que é ELK?

![Flow_Fleet_Elasticsearch.png](../../../img/tools_imgs/flow_fleet_elasticsearch.png)
Fonte: <a target="_blank" href="https://www.elastic.co/guide/en/fleet/current/add-fleet-server-on-prem.html">Elastic Documentation</a>


A imagem acima ilustra o fluxo de dados e a integração dos componentes do ELK Stack para monitoramento centralizado e análise em tempo real.

- **Elasticsearch**: Responsável por armazenar e indexar os dados recebidos do Fleet Server. Com capacidade de busca e análise em tempo real, o Elasticsearch é o núcleo do ELK Stack, permitindo consultas eficientes em grandes volumes de dados e facilitando uma análise detalhada.

- **Kibana**: O Kibana Oferece uma interface gráfica onde os dados no Elasticsearch podem ser visualizados e analisados. Kibana também gerencia os pacotes e integrações disponíveis para os agentes, que podem ser carregados a partir do Package Registry. Com ele, é possível criar dashboards, relatórios e gráficos, transformando dados brutos em insights visuais.

- **Elastic Agent**: Localizados nos dispositivos a serem monitorados, os Elastic Agents coletam dados de logs, métricas e eventos e os enviam ao Fleet Server Cluster. Esses agentes são configurados e gerenciados por políticas que controlam quais dados são coletados e para onde são enviados.

- **Fleet Server Cluster**: Utilizando um balanceador de carga para alta disponibilidade, o Fleet Server Cluster centraliza o gerenciamento dos Elastic Agents. Ele distribui políticas para os agentes, garantindo uma coleta consistente de dados, e depois os encaminha ao Elasticsearch para armazenamento e análise.


Esse fluxo garante que os dados da rede sejam coletados de forma unificada, armazenados de maneira otimizada e disponibilizados para visualização e análise, oferecendo uma solução completa e robusta para monitoramento e análise de redes complexas e distribuídas.

!!! warning "Observação"
    nesta instalação não utilizaremos o **Logstash**, e sim a versão mais morderna de coleta, no qual são os **Fleet Server** e **Fleet Agent**,
    para saber mais acesse a documentação oficial sobre Fleet: <a href="https://www.elastic.co/guide/en/fleet/current/fleet-overview.html" target="_blank">Documentação do Elastic - Fleet</a>

---

## :octicons-checklist-24: 4. Pré-requisitos

Antes de prosseguir com a configuração do ELK, é necessário configurar a rede **br-lab**. Para detalhes sobre essa configuração, consulte o guia [**Primeiros Passos: Preparando o Ambiente**](../Primeiros passos - preparando o ambiente.md).

---

## :octicons-tools-24: 5. Preparando o Ambiente

Após garantir que a rede **br-lab** está configurada, siga os passos abaixo para preparar o ambiente de trabalho.

## :fontawesome-brands-docker: 6. Baixando o Docker Compose

Para baixar o Docker Compose, execute o seguinte comando:

=== "Linux/ Mac"

    ```bash
        curl -L -o get.sh "https://git.rnp.br/redes-abertas/docker-composes/-/raw/main/ELK-Stack/get.sh?inline=false" && sh get.sh && cd ELK-Stack
    ```

=== "Windows"
    ```bash
        curl -L -o get.bat "https://git.rnp.br/redes-abertas/docker-composes/-/raw/main/ELK-Stack/get.bat?inline=false" && call get.bat && cd ELK-Stack
    ```

Esse comando faz o download do script de instalação e, em seguida, navega para o diretório **ELK-Stack**.

## :octicons-container-24: 7. Subindo os Containers

Após baixar o Docker Compose, execute o comando abaixo para iniciar os serviços do ELK:

```bash
docker compose up -d
```

Esse comando irá iniciar três containers essenciais para o funcionamento do stack ELK:

1. **Elasticsearch**
    - **Descrição**: Motor de busca e armazenamento de dados. Ele permite o armazenamento de documentos em formato JSON e fornece uma API RESTful para busca e análise. Ideal para pesquisa em grandes volumes de dados.
    - **IP**: `172.10.10.201`
    - **Porta padrão**: `9200`
    - **Documentação**: <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html" target="_blanck">Elasticsearch Documentation</a>
2. **Kibana**
    - **Descrição**: Interface gráfica para visualização de dados armazenados no Elasticsearch. O Kibana permite que os usuários criem dashboards interativos e visualizações de dados em tempo real, facilitando a análise e interpretação de dados.
    - **IP**: `172.10.10.202`
    - **Porta padrão**: `5601`
    - **Documentação**: <a href="https://www.elastic.co/guide/en/kibana/current/index.html" target="_blanck">Kibana Documentation</a>
3. **Fleet Server**
    - **Descrição**: Agente responsável pela coleta de métricas e logs de diferentes fontes e seu envio para o Elasticsearch. O Fleet Server facilita a gestão centralizada de agentes de coleta, como o Elastic Agent, permitindo a coleta e envio eficiente de dados.
    - **IP**: `172.10.10.203`
    - **Documentação**: <a href="https://www.elastic.co/guide/en/fleet/current/index.html" target="_blanck">Fleet Server Documentation</a>
!!! info "Acesso"
    :material-access-point: Usuario e senha padrão
    - **Usuário padrão**: `elastic`
    - **Senha padrão**: `admin@123`

!!! tip "Configuração"
    Para alterar a senha ou a versão do Elasticsearch, edite o arquivo **.env**.

## :simple-kibana: 8. Acessando a Interface do Kibana

Para acessar a interface do Kibana, use o seguinte link:

```
https://<seu-ip>:5601
```

Faça login com o usuário e senha padrão.

## :material-skip-next-outline: Próximos Passos

- **Configurar a Coleta IPFIX**: Após a configuração do ELK, o próximo passo será configurar a coleta de dados utilizando o IPFIX, com nosso guia de [configuração de IPFIX](Configurando IPFIX no ELK.md).

