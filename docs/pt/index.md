# **Home**

**Bem-vindo ao projeto Redes Abertas!**

Este projeto tem como objetivo fornecer uma base sólida para a configuração e simulação de redes utilizando ferramentas modernas e eficientes: **NetBox**, r**Netreplica** e **Containerlab**.

O projeto **Redes Abertas** foi desenvolvido para profissionais e entusiastas da área de redes que desejam:

- **Explorar**: Testar diferentes configurações de rede em um ambiente controlado.
- **Automatizar**: Utilizar templates para padronizar e automatizar as configurações de dispositivos de rede.
- **Replicar**: Reproduzir ambientes de rede reais em laboratórios virtuais para testes e validações.
- **Gerenciar**: Centralizar a documentação e o gerenciamento de infraestruturas de rede de maneira eficiente.

Com essas ferramentas, o projeto visa simplificar a criação, gerenciamento e documentação de topologias de rede complexas, proporcionando flexibilidade e escalabilidade.

---

## Capacidades do Containerlab

**Containerlab** é uma ferramenta poderosa para a criação e gerenciamento de laboratórios de rede virtualizados, utilizando contêineres Docker. Com ela, você pode testar e simular topologias de rede complexas em um ambiente controlado. A ferramenta suporta diversos dispositivos de rede, permitindo a configuração de redes **multivendor**, o que é ideal para testar interações entre diferentes fornecedores em um mesmo laboratório.
Abaixo uma lista dos principais vendors suportados pelo Containerlab:
![Vendors](../img/vendors.svg)

---

## Fluxograma dos Laboratórios

O fluxograma ilustra o fluxo de trabalho do **Netreplica** no contexto de um ambiente de simulação de rede, em integração com o **Containerlab**:

![Workflow Netreplica](../img/tools_imgs/workflow-netreplica.gif)

---

## Estrutura do Fluxo de Trabalho

### 1. **Topologia**

A topologia de rede define a estrutura e interconexão dos dispositivos de rede.

### 2. **NetBox**

A topologia é documentada e gerenciada no **NetBox**, uma plataforma centralizada para gerenciamento de infraestrutura de rede. O NetBox armazena informações detalhadas sobre dispositivos, endereços IP e conexões físicas.

### 3. **Netreplica**

O **Netreplica** sincroniza as informações de configuração do NetBox e prepara os dados para a simulação. Ele obtém os dados via API e gera arquivos de configuração YAML necessários para a simulação.

### 4. **Configurações**

O **Netreplica** gera arquivos de configuração YAML detalhados que descrevem como os dispositivos de rede devem ser configurados.

### 5. **Containerlab**

O **Containerlab** utiliza os arquivos de configuração gerados para criar e gerenciar topologias de rede complexas em contêineres Docker.

### 6. **Laboratório (Stack Docker)**

A simulação é executada em um ambiente de laboratório utilizando um stack Docker. A topologia definida é reproduzida, permitindo testes e validações.

### 7. **Graphite**

Para monitorar e visualizar métricas e desempenho da simulação, o **Graphite** é integrado ao laboratório. Ele coleta e exibe dados relevantes para análise.

---

## Resumo do Fluxo

1. **Definição da Topologia**: A estrutura e interconexão dos dispositivos de rede são definidas.
2. **Documentação no NetBox**: A topologia é documentada e gerenciada no **NetBox**.
3. **Sincronização com Netreplica**: O **Netreplica** sincroniza as informações do **NetBox** via API e gera configurações YAML.
4. **Criação de Topologia com Containerlab**: O **Containerlab** usa as configurações YAML para criar a topologia de rede em contêineres Docker.
5. **Execução da Simulação**: A topologia é executada em um ambiente de laboratório Docker.
6. **Monitoramento com Graphite**: O desempenho e as métricas da simulação são monitorados e visualizados com **Graphite**.

---

## Status do Projeto

Projeto em andamento.

---

## Getting Started
Para começar, leia o [Guia de Configuração](./Getting%20Started.md) para aprender como utilizar as ferramentas NetBox, Containerlab e Netreplica em conjunto.

---

## Laboratórios Disponíveis

- [Roteamento OSPF](Laboratórios/Juniper/vMX/Roteamento-OSPF/index.md) - Laboratório de Configuração de OSPF baseados na plataforma MX da Juniper em uma topologia em anel.
- [Descoberta](Laboratórios/Juniper/vJunos/Descoberta/index.md) - Laboratório de descoberta de dispositivos de rede utilizando OSPF e SNMP, integrando Zabbix e NetBox.
- [Monitoramento ELK](Laboratórios/Juniper/vJunos/Monitoramento-ELK/index.md) - Laboratório de monitoramento de fluxos IPFIX utilizando o Elastic Stack (Elasticsearch, Kibana, Fleet Server e Elastic Agent).
- [Monitoramento Telegraf](Laboratórios/Juniper/vJunos/Monitoramento-Telegraf/index.md) - Laboratório de monitoramento de fluxos de tráfego via Telegraf/IPFIX para InfluxDB.
- [Monitoramento Zabbix](Laboratórios/Juniper/vJunos/Monitoramento-Zabbix/index.md) - Laboratório de monitoramento de roteadores via SNMP com coleta centralizada pelo Zabbix Server.
- [Configuração NETCONF](Laboratórios/Multivendor/Configuração-NETCONF/index.md) - Laboratório de configuração de dispositivos via NETCONF.
---

## Ferramentas

- [NetBox](Getting Started.md): Ferramenta para gerenciamento de infraestrutura de rede
- [Containerlab](Getting Started.md): Ferramenta para simulacão de topologias de rede complexas
- [Netreplica](Getting Started.md): Ferramenta para replicação de ambientes de rede do NetBox para o Containerlab
- [ELK](Ferramentas/Elasticsearch/index.md): Stack para monitoramento de logs e Fluxos de dados em tempo real
- [Edgeshark](Ferramentas/Edgeshark/index.md): Ferramenta para captura e visualização de tráfego de rede
- [LibreNMS](Ferramentas/LibreNMS/index.md): Ferramenta para monitoramento de dispositivos de rede


---

## Contribua

Contribua com o projeto clicando [aqui](Contribua.md).

---