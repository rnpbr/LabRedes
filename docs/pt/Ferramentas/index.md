# Ferramentas

## :octicons-book-24: **Introdução**

Antes de começar a usar as ferramentas de monitoramento, é fundamental configurar a base de comunicação entre os seus laboratórios. Para isso, utilizamos uma rede Docker dedicada chamada **br-lab**. A rede **br-lab** facilita a integração de ferramentas de análise com os laboratórios criados no Containerlab, eliminando a necessidade de configurar repetidamente cada ferramenta para diferentes laboratórios.

### :octicons-gear-24: **Passo 1: Configuração da Rede Docker br-lab**

Acesse o [Guia de Configuração da Rede br-lab](Primeiros passos - preparando o ambiente.md) para configurar sua rede Docker. Essa rede será responsável por conectar seus laboratórios ao sistema de monitoramento de forma eficiente, permitindo que múltiplas ferramentas funcionem de maneira integrada.

---

## :octicons-search-24: **Passo 2: Escolhendo a Ferramenta de Monitoramento**

Após configurar a rede **br-lab**, você poderá selecionar a ferramenta que melhor atenda às suas necessidades. Cada uma das ferramentas listadas abaixo oferece funcionalidades específicas para diferentes tipos de monitoramento, seja de dispositivos de rede, tráfego ou logs.

### :material-compare-horizontal: **Comparação de Ferramentas**

A tabela a seguir oferece uma visão geral das ferramentas que cobrimos em nossos tutoriais, destacando seus principais recursos, tipo de monitoramento e opções de preço:

### **Tabela: Comparação de Ferramentas de Monitoramento**

| **Ferramentas** | **Tecnologias de coleta e integração** | **Custo** | **Dificuldade de Implementação** | **Integrações** | **Ponto Forte** | **Comunidade/Documentação** |
| --- | --- | --- | --- | --- | --- | --- |
| **Zabbix** | <a target="_blank" href="https://www.zabbix.com/documentation/current/manual/appendix/protocols">SNMP, ICMP, JMX, IPMI, API_rest, Agent</a>, | <a target="_blank" href="https://www.zabbix.com/pricing">Gratuito</a> | <a target="_blank" href="https://www.zabbix.com/documentation/current/manual/quickstart/installation">Fácil</a> | <a target="_blank" href="https://www.zabbix.com/integrations?cat=logfiles">Grafana, prometheus,elastic, kafka, Graylog, ..etc</a> | <a target="_blank" href="https://www.zabbix.com/documentation/current/manual/config/notifications">Alertas avançados</a> | <a target="_blank" href="https://www.zabbix.com/community">Completa</a> |
| **ELK Stack** | <a target="_blank" href="https://www.elastic.co/integrations/data-integrations">Syslog, IPFIX , Netflow, SNMP, ICMP</a>  | <a target="_blank" href="https://www.elastic.co/pricing/">Freemium</a> | <a target="_blank" href="https://www.elastic.co/guide/en/observability/current/monitoring-getting-started.html">Moderada</a> | <a target="_blank" href="https://www.elastic.co/integrations/data-integrations">Fleet, logstash, filebeat, grafana, .etc</a> | <a target="_blank" href="https://www.elastic.co/kibana/kibana-dashboard">Análise centralizada de logs, Dashboard prontos</a> | <a target="_blank" href="https://www.elastic.co/docs">Completa</a> |
| **Telegraf + InfluxDB + Grafana** | <a target="_blank" href="https://docs.influxdata.com/telegraf/v1/plugins/">SNMP, IPFIX, SFLOW, Syslog, gMNIC, Netflow, GRPC, etc</a> | <a target="_blank" href="https://www.influxdata.com/products/pricing/">Freemium</a> | <a target="_blank" href="https://grafana.com/docs/grafana/latest/setup-grafana/installation/">Moderado</a> | <a target="_blank" href="https://grafana.com/docs/grafana/latest/datasources/">Prometheus, Loki,</a>  | <a target="_blank" href="https://www.influxdata.com/time-series-platform/">Stack modular e escalável</a> | <a target="_blank" href="https://docs.influxdata.com">Ampla</a> |
| **LibreNMS** | <a target="_blank" href="https://docs.librenms.org/Support/Configuration/">SNMP, Syslog, API_Rest</a> | <a target="_blank" href="https://www.librenms.org/#pricing">Gratuito</a> | <a target="_blank" href="https://docs.librenms.org/Installation/">Fácil</a> | <a target="_blank" href="https://docs.librenms.org/Extensions/Applications/">Grafana, Graylog, Proxmox</a> | <a target="_blank" href="https://docs.librenms.org/Support/Features/">Autodiscovery</a> | <a target="_blank" href="https://docs.librenms.org">Média</a> |

---

## :material-test-tube: **Passo 3: Implementação e Testes**

Após selecionar a ferramenta mais adequada, siga os tutoriais específicos para configurar e integrar a solução escolhida com seu ambiente de rede criado no **Containerlab**. Cada guia oferece instruções passo a passo para garantir uma integração suave e funcional das ferramentas de monitoramento com seus laboratórios.

### :octicons-tools-24: **Exemplos de Cenários de Teste**:

- **Monitoramento de Dispositivos de Rede com LibreNMS**: Configure LibreNMS para monitorar switches e roteadores dentro do seu laboratório.
- **Análise de Logs e Eventos com ELK Stack**: Colete e visualize dados de logs gerados por dispositivos da rede.
- **Captura de Pacotes com EDSHARK**: Execute diagnósticos de rede e analise pacotes capturados diretamente dos roteadores.

---

## :material-ip-network: **Configuração de Rede br-lab e Endereços Fixos**

Todas as ferramentas são configuradas para serem atreladas à rede **br-lab** e para facilitar o uso delas, independentemente do laboratório, elas possuem IPs fixos. Esses IPs podem ser consultados na lista abaixo, permitindo que você se conecte diretamente a cada ferramenta sem a necessidade de configurações adicionais para cada novo laboratório.

### **Tabela: IPs Fixos das Ferramentas**

| Serviço | IP | Stack |
| --- | --- | --- |
| librenms-db | 172.10.10.100 | librenms |
| librenms-redis | 172.10.10.101 | librenms |
| librenms-msmtpd | 172.10.10.102 | librenms |
| librenms-librenms | 172.10.10.103 | librenms |
| librenms-dispatcher | 172.10.10.104 | librenms |
| librenms-syslogng | 172.10.10.105 | librenms |
| librenms-snmptrapd | 172.10.10.106 | librenms |
| elk-setup | 172.10.10.107 | ELK |
| elk-elasticsearch | 172.10.10.108 | ELK |
| elk-kibana | 172.10.10.109 | ELK |
| elk-fleet-server | 172.10.10.110 | ELK |
| grafana-grafana | 172.10.10.111 | Grafana |
| grafana-influxdb | 172.10.10.112 | Grafana |
| grafana-chronograf | 172.10.10.113 | Grafana |
| grafana-telegraf | 172.10.10.114 | Grafana |
| zabbix-server | 172.10.10.115 | Zabbix |
| zabbix-frontend | 172.10.10.116 | Zabbix |
| zabbix-agent | 172.10.10.117 | Zabbix |
| zabbix-database | 172.10.10.118 | Zabbix |

Esses IPs fixos garantem uma comunicação estável e facilitada entre as ferramentas e os laboratórios configurados no **Containerlab**. Com isso, você pode integrar múltiplas ferramentas de monitoramento de forma eficiente, sem precisar redefinir configurações de rede a cada novo laboratório.

---

Essa adição inclui a configuração de rede Docker, a explicação sobre os IPs fixos e como eles facilitam a integração das ferramentas no seu ambiente de laboratório.

## :material-tools: **Ferramentas Futuras**

Estamos constantemente testando e adicionando novas ferramentas ao nosso repertório. Algumas opções que consideramos explorar em breve incluem:

- **Prometheus**: Servidor de monitoramento e visualização de dados.
- **OpenElastic**: Uma solução escalável e flexível para auditoria de logs e eventos, baseada no Elastic Stack.
- **OpenNMS**: Ferramenta robusta para monitoramento de redes e sistemas, com foco em redes de grande escala.
- **Akivorado**: Ferramenta de monitoramento de fluxo de dados para redes.

Essas ferramentas podem ser integradas ao seu ambiente de laboratório com o **Containerlab**, 
permitindo que você crie um ecossistema robusto para gerenciamento e análise de redes.

---