# Guia de Instalação do Telegraf

## :octicons-book-24: 1. Introdução

Este guia apresenta a instalação do **Telegraf**, uma ferramenta de coleta de métricas que será utilizada no laboratório **br-lab**. O Telegraf fornece suporte a diversos protocolos e plugins para coleta de métricas, permitindo sua integração com diferentes sistemas e dispositivos. A instalação utiliza o Docker Compose para provisionar automaticamente os serviços necessários, garantindo uma implementação prática e eficiente no ambiente do laboratório.

---

## :material-network: 2. O que é o Telegraf?

O Telegraf é um agente de coleta de métricas altamente configurável desenvolvido pela **InfluxData**. Ele é compatível com uma ampla variedade de protocolos e plugins, o que possibilita capturar e processar métricas de sistemas, dispositivos, aplicações e serviços em tempo real.

### principais Componentes:

1. **Telegraf**: Agente de coleta de dados configurável.
2. **InfluxDB**: Banco de dados de séries temporais onde os dados do Telegraf serão armazenados.
3. **Grafana**: Ferramenta para visualização e análise dos dados coletados.
4. **Chronograf**: Interface gráfica adicional para consulta e análise de dados no InfluxDB.

Essa arquitetura integra captura, armazenamento e visualização de métricas, garantindo flexibilidade e eficiência no monitoramento do ambiente.

---

## :octicons-checklist-24: 3. Pré-requisitos

Certifique-se de atender aos seguintes pré-requisitos antes da instalação:

1. **Rede br-lab configurada**:
    - A rede **br-lab** é obrigatória para isolar os serviços no ambiente. Para mais detalhes sobre essa configuração, consulte o guia [**Primeiros Passos: Preparando o Ambiente**](../Primeiros passos - preparando o ambiente.md).

2. **Pacotes Necessários**:
    - `docker`, `docker-compose`, `curl`.


## :fontawesome-brands-docker: 4. Preparando o Ambiente

### 4.1. Baixando o Script de Instalação

Execute o comando abaixo para baixar e configurar os serviços necessários:
=== "Linux/ Mac"

    ```bash
        curl -L -o get.sh "https://git.rnp.br/redes-abertas/docker-composes/-/raw/main/Telegraf/get.sh?inline=false" && sh get.sh && cd Telegraf
    ```

=== "Windows"
    ```bash
        curl -L -o get.bat "https://git.rnp.br/redes-abertas/docker-composes/-/raw/main/Telegraf/get.bat?inline=false" && call get.bat && cd Telegraf
    ```

Esse comando:

- Baixará o arquivo do Docker Compose contendo a configuração dos serviços.
- Criará o diretório **Telegraf**, onde os arquivos necessários serão armazenados.

---

## :octicons-container-24: 5. Subindo os Containers

Para iniciar os serviços do Telegraf e seus componentes, execute:

```bash
docker compose up -d
```

Isso iniciará os seguintes containers:

1. **Telegraf**: Agente de coleta de dados com suporte a vários protocolos e formatos.
    - **IP**: `172.10.10.114`
    - **Volumes mapeados**:
        - Configuração do Telegraf.
        - Diretórios do sistema do host (*proc*, *sys*, *etc*).
    - **Documentação**: <a href="https://docs.influxdata.com/telegraf/v1/get-started/" target="_blanck">Telegraf Documentation</a>

2. **InfluxDB**: Banco de dados para armazenar as métricas coletadas pelo Telegraf.
    - **IP**: `172.10.10.112`
    - **Credenciais de acesso**:
        - **Username**: `admin`
        - **Senha**: `admin`
    - **Base de dados padrão**: `telemetry`
    - **Documentação**: <a href="https://docs.influxdata.com/influxdb/v1/" target="_blanck">InfluxDB Documentation</a>

3. **Grafana**: Interface gráfica para visualização de métricas armazenadas no InfluxDB.
    - **IP**: `172.10.10.111`
    - **Porta Padrão**: `3000`
    - **Credenciais**:
        - **Usuário**: `admin`
        - **Senha**: `admin`
    - **Documentação**: <a href="https://grafana.com/docs/grafana/latest/fundamentals/" target="_blanck">Grafana Documentation</a>

4. **Chronograf**: Ferramenta adicional para consultas e análises visuais no InfluxDB.
    - **IP**: `172.10.10.113`
    - **Porta Padrão**: `8888`
    - **Documentação**: <a href="https://docs.influxdata.com/chronograf/v1/" target="_blanck">Chronograf Documentation</a>

Para verificar o status de execução dos containers:

```bash
docker compose ps
```

---

## :fontawesome-solid-chart-line: 6. Acessando os Componentes

### 6.1. Acesso ao Grafana

Após inicializar os serviços, o Grafana estará acessível pelo endereço:

```
http://<IP_DO_SERVIDOR>:3000
```

Faça login utilizando as credenciais padrão abaixo:

- **Usuário**: `admin`
- **Senha**: `admin`

### 6.2. Acesso ao Chronograf

O Chronograf pode ser acessado em:

```
http://<IP_DO_SERVIDOR>:8888
```

Use as credenciais configuradas no InfluxDB para acessar e configurar consultas.

## :octicons-rocket-24: 8. Próximos Passos

- **Criar Dashboards personalizados no Grafana**: Explore as métricas para criar visualizações específicas para suas necessidades.
- **Adicionar Fontes de Dados ao Telegraf**: Amplie o uso configurando o Telegraf para coletar métricas de outras fontes de interesse no laboratório.

Para mais informações sobre o Telegraf, consulte a <a target="_blank" href="https://github.com/influxdata/telegraf">documentação oficial do Telegraf</a>.