# :material-bookmark: Multvendor logs Telegraf

Este laboratório simula, via Containerlab, a interligação entre três roteadores Juniper, Huawei e Cisco, com roteamento dinâmico via OSPF, exportação de logs via Syslog usando Telegraf, InfluxDB, Chronograf e Grafana.

---

## :material-bookmark: 1. Descrição

### :octicons-goal-16: 1.1 Objetivo do Lab

O objetivo do laboratório é simular a exportação de logs de três roteadores de diferentes fabricantes (Juniper, Huawei e Cisco) para um servidor de monitoramento centralizado, utilizando o protocolo Syslog. O sistema de monitoramento é composto por Telegraf, InfluxDB, Chronograf e Grafana, permitindo a coleta, armazenamento e visualização de métricas de rede em tempo real.

### :material-lan: 1.2 Topologia do Lab

![Topologia do Lab](../../../../img/labs_imgs/Topologia_Logs_Telegraf.svg)

**Descrição da Topologia**

* Três roteadores (Juniper, Cisco, Huawei) interligados em topologia em anel com links ponto a ponto /31.
* Roteamento dinâmico via OSPF entre os roteadores.
* Coleta de logs via Syslog udp (514).
* Observabilidade com a pilha TICK (Telegraf, InfluxDB, Chronograf) e Grafana.
* Rede externa `br-lab` conecta os nós à infraestrutura de monitoramento.

---

## :octicons-search-16: 2. Aplicações

### Exemplos de Aplicações

Este laboratório pode ser explorado em diversos cenários acadêmicos e de pesquisa aplicada, servindo como base para experimentação de monitoramento e visualização de tráfego em redes com múltiplos roteadores.

#### Possíveis Aplicações:

* **Treinamento de equipes de NOC em ambiente multivendor**: Simula operações reais com roteadores Juniper, Huawei e Cisco, utilizando OSPF e exportação de logs via Syslog, permitindo análise de conectividade e resolução de falhas.
* **Validação e testes de coleta de logs via Syslog**: Permite verificar a compatibilidade e o comportamento de diferentes vendors no envio de logs para Telegraf.
* **Visualização e análise de métricas em tempo real**: Validar e testar formas de templates do grafana para trabalhar com logs.
* **Monitoramento centralizado com Telegraf**: Avalia a capacidade do Telegraf de receber e processar logs de dispositivos heterogêneos, garantindo integridade e consistência dos dados.
* **Ensino de integração de sistemas de monitoramento**: Proporciona aprendizado prático sobre configuração de Syslog, coleta de métricas e visualização em pilhas TICK e Grafana em um cenário multivendor.
---

## :material-tools: 3. Requisitos

Abaixo estão listados os requisitos mínimos de hardware e software necessários para executar o laboratório. Certifique-se de incluir as ferramentas essenciais, como **Containerlab** e **Docker**, além da rede `br-lab` previamente criada.
para saber mais sobre este itens acesse:

- [Criação da Rede br-lab](../../../../Ferramentas/Primeiros passos - preparando o ambiente.md)
-  <a target="_blank" href="https://www.docker.com/get-started/">Instalação do Docker</a>
-  <a target="_blank" href="https://containerlab.dev/install/">Instalação do containerlab</a>

E tenha a stack telegraf previamente instalado, para saber mais sobre a instalação do zabbix acesse: [Instalação do Telegraf](../../../../Ferramentas/Telegraf/index.md)

### :material-alert: Tabela de Requisitos Minimos:

| Requisito           | Detalhes              |
| ------------------- |-----------------------|
| **CPUs**            | 4 vCPUs               |
| **Memória RAM**     | 8 GB                  |
| **Espaço em Disco** | 10 GB (recomendado)   |
| **Containerlab**    | 0.45.0 ou superior    |
| **Docker Engine**   | 23.0.3 ou superior    |
| **Imagens**         | `vr-vjunos:23.2R1.14`, `vrnetlab/huawei_vrp:ne40e-8.180`, `xrd-control-plane:7.10.2` |
| **Rede Docker**     | `br-lab`              |

!!! warning "Atenção" 
    Verifique se o seu processador possui **suporte à virtualização por hardware** e se essa funcionalidade está **ativada na BIOS/UEFI**.  
    - Em processadores **Intel**, essa tecnologia é chamada de **VT-x** (Intel Virtualization Technology).  
    - Em processadores **AMD**, é conhecida como **AMD-V** (AMD Virtualization).  

    Sem essa funcionalidade ativada, as imagens como o **vJunos-router** não funcionarão corretamente.
---

## :fontawesome-solid-prescription-bottle: 4. Implantando o Lab

Você pode realizar a implantação por meio de um script pronto ou configurar manualmente os arquivos do lab.

### :material-git: 4.1 Implantação Pronta

Este método permite ao usuário **baixar uma versão pré-montada** do laboratório, com a topologia e as configurações já definidas. Basta baixar o repositório e seguir para o início da execução.

!!! tip "Dica" 
    A implantação pronta é útil para quem deseja começar rapidamente com um ambiente configurado.

#### :octicons-download-16: Baixando o Lab

Execute o script abaixo para baixar e configurar o laboratório automaticamente:

=== "Linux/Mac"

    ```bash
    curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/logs-telegraf-multvendor/get.sh" && sh get.sh && cd logs-telegraf-multvendor
    ```

=== "Windows"

    ```bat
    curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/logs-telegraf-multvendor/get.bat" && call get.bat && cd logs-telegraf-multvendor
    ```

!!! tip "Dica"
    No Linux/Mac, use `chmod +x get.sh` antes de executar o script, caso ele não esteja com permissão de execução.

---

## :octicons-play-16: 5. Inicializando o Lab

Após o download ou personalização, siga as etapas abaixo para **iniciar o laboratório**.
Execute o comando abaixo dentro do diretório baixado.

```bash
sudo containerlab deploy
```

Esse comando criará os containers dos roteadores, configurará os links e iniciará os serviços de monitoramento.

!!! tip "Depuração"
    Use `docker logs -f <nome_container>` para verificar o estado dos serviços, caso algo não funcione.

---

## :material-access-point: 6. Acesso aos Dispositivos

### :material-table: 6.1 IPs e Portas dos Serviços

| Dispositivo     | IP de Acesso  | Porta(s) | Serviço            |
| --------------- | ------------- |-----| ------------------ |
| **node1**           | 172.10.10.201 | 22      | SSH               |
| **node2**           | 172.10.10.202 | 22      | SSH               |
| **node3**           | 172.10.10.203 | 22      | SSH               |
| **Telegraf**    | 172.10.10.114 | 161 | Coleta de métricas |
| **InfluxDB**    | 172.10.10.112 | 8086 | Banco de séries    |
| **Chronograf**  | 172.10.10.113 | 8888 | UI de análise      |
| **Grafana**     | 172.10.10.111 | 3000 | Dashboard Web      |
| **Graphite** | 172.10.10.119 | 8080    | Web UI (Graphite) |

### :material-key-link: 6.2 Senhas de Acesso

| Serviço          | Usuário | Senha             |
| ---------------- | ------- |-------------------|
| **node1 (SSH)**     | `admin`  | `admin@123`      |
| **node2 (SSH)**     | `clab`   | `clab@123`       |
| **node3 (SSH)**     | `admin`  | `admin`          |
| Grafana          | `admin` | `admin`           |
| InfluxDB         | `admin` | `influxpassword`  |

!!! warning "Verificação de Inicialização"
    Antes de acessar os serviços, use `docker ps` e verifique os logs dos containers para garantir que estão funcionando corretamente.

---

## :octicons-browser-16: 7. Observabilidade e Visualização

!!! Warning "Atenção"
    Devido à forma como as configurações são aplicadas no vJunos-router, a configuração do syslog deve ser feita manualmente.
    Siga o passo a passo abaixo para enviar todos os logs do sistema para o servidor de logs remoto.

### Passo a passo

Acesse o node1 via ssh e execute:

```junos
configure
```

* Entra no **modo de configuração** do Junos.
* Todos os comandos seguintes vão alterar a configuração do equipamento.

```junos
set system syslog host 172.10.10.114 any any
```

* Define o servidor de logs remoto (**172.10.10.114**) como destino.
* `any any` significa: enviar **qualquer facility** (sistema, kernel, daemon, auth etc.) em **qualquer nível de severidade** (emergency, alert, critical, warning, info, debug).
* Na prática: **todos os eventos do sistema serão enviados para esse servidor**.

```junos
set system syslog source-address 172.10.10.201
```

* Define o **IP de origem** dos pacotes de log como **172.10.10.201** (o IP do vJunos-router).
* Isso garante que o tráfego de syslog saia pela interface que possui esse endereço.
* É importante para o servidor de logs reconhecer corretamente a origem das mensagens.

```junos
commit
```

* Aplica as alterações feitas na configuração.

!!! warning "atenção"
    Após o inicio do Vjunos, pode levar entre 3 a 6 minutos para subir todas as rotas e a configuração funcionar corretamente.


* Somente após esse comando os logs começam a ser enviados para o destino configurado.




### 7.1 Telegraf

O Telegraf está configurado para coletar métricas via:

* **syslog**: exportação de logs 
* **IPFIX**: exportação de fluxos de tráfego.


### 7.2 InfluxDB

Banco de séries temporais onde as métricas do Telegraf são armazenadas. Pode ser acessado pela porta 8086.

### 7.3 Chronograf

Interface web de análise de métricas armazenadas no InfluxDB. Acessível em `http://172.10.10.113:8888`.

### 7.4 Grafana

Plataforma de visualização interativa onde os dados são apresentados em dashboards personalizados.


