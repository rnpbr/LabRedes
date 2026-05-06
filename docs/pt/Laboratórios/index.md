# Containerlab

**Containerlab** é uma ferramenta poderosa para criar e gerenciar laboratórios de rede virtualizados. Com ele, você pode simular topologias de rede complexas utilizando contêineres Docker. A seguir, você encontrará informações sobre os pré-requisitos, ferramentas recomendadas e como documentar seus laboratórios.

---

## Pré-requisitos

Antes de começar a utilizar o Containerlab, certifique-se de ter os seguintes pré-requisitos instalados:

### Docker

- O Docker é utilizado pelo Containerlab para criar e executar os contêineres que compõem a rede virtualizada.
- **Link**: <a target="_blank" href="https://www.docker.com/get-started/">Documentação oficial do Docker</a>.

### Containerlab

- Instale o Containerlab conforme as instruções fornecidas na documentação oficial.
- **Link**: <a target="_blank" href="https://containerlab.dev/install/">Documentação oficial do Containerlab</a>.

---

## Labs Disponíveis

Aqui está um exemplo de laboratório configurado para simular OSPF utilizando Junos:

### Roteamento OSPF (Junos)

- Simulação de OSPF com Junos, uma das tecnologias de roteamento mais utilizadas.
- **Link**: [Roteamento OSPF (Junos) Lab](Juniper/vMX/Roteamento-OSPF/index.md).

### Descoberta (Junos)

- Importação de roteadores com scripts, utilizando Zabbix e Netbox.
- **Link**: [Descoberta (Junos) Lab](Juniper/vJunos/Descoberta/index.md).

### Monitoramento ELK (Junos)
- Exportação de fluxos IPFIX para Elasticsearch com Elastic Agent.
- Visualização dos fluxos em tempo real com dashboards no Kibana.
- **Link**: [Monitoramento ELK (Junos)](Juniper/vJunos/Monitoramento-ELK/index.md).

### Monitoramento Telegraf (junos)
- Exportação de fluxos de tráfego via Telegraf/IPFIX para InfluxDB.
- Dashboards prontos no Grafana para análise de tráfego por interface e protocolo.
- **Link**: [Monitoramento Telegraf (Junos)](Juniper/vJunos/Monitoramento-Telegraf/index.md).

### Monitoramento Zabbix (junos)
- Monitoramento de roteadores via SNMP com coleta centralizada pelo Zabbix Server.
- Permite visualização de métricas e alertas em tempo real no frontend do Zabbix.
- **Link**: [Monitoramento Zabbix (Junos)](Juniper/vJunos/Monitoramento-Zabbix/index.md).
---

## Ferramentas de Análise Recomendadas

Além do Containerlab, você pode utilizar as seguintes ferramentas de análise para monitorar e depurar sua rede virtualizada:

### LibreNMS

- Uma plataforma de monitoramento de rede baseada na web, que fornece insights sobre o desempenho e a saúde da rede. Ideal para monitoramento contínuo da rede em tempo real.

### Wireshark

- Ferramenta de captura e análise de pacotes que permite examinar o tráfego de rede em detalhes. Essencial para depuração e análise de protocolos de rede.

além destas ferramentas mencionadas ha outras que podem ser configuradas conforme suas necessidades, para saber mais acesse: [Ferramentas de Análise](../Ferramentas/index.md).


---

## Documentando Seus Labs

Para garantir que seus laboratórios sejam bem documentados e fáceis de entender, consulte a seção sobre **Documentação de Labs**. Lá, você encontrará boas práticas e exemplos para criar documentação clara e útil para os seus ambientes simulados.

- **Link**: [Documentação de Labs](Contribua/index.md).