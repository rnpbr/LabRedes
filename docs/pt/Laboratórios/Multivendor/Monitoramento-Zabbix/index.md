# :material-bookmark: Multvendor Monitoramento Zabbix

 Este laboratório, utilizando o Containerlab, simula a interconexão de três roteadores de diferentes fabricantes: vJunos (Juniper), Huawei VRP e Cisco XRD. 

---

## :material-bookmark: 1. Descrição

### :octicons-goal-16: 1.1 Objetivo do Lab

O laboratório “Multvendor Monitoramento Zabbix” demonstra a simulação da interconexão de três roteadores de diferentes fabricantes — vJunos (Juniper), Huawei VRP e Cisco XRD — utilizando o Containerlab. Os dispositivos estão interconectados em topologia em anel e o roteamento é realizado pelo protocolo OSPF, permitindo a troca dinâmica de rotas. A comunicação com o Zabbix ocorre via SNMP, possibilitando o monitoramento em tempo real.

### :material-lan: 1.2 Topologia do Lab

![Topologia do Lab](../../../../img/labs_imgs/Topologia_Multvendor_Zabbix.svg)

A topologia deste laboratório é composta por três roteadores interconectados em topologia em anel, permitindo comunicação direta entre os dispositivos. Cada roteador está configurado com OSPF, garantindo o roteamento dinâmico entre as interfaces. O monitoramento é realizado a partir de uma rede externa denominada br-lab, à qual os roteadores estão conectados por interfaces virtuais. Essa configuração possibilita que o Zabbix monitore a conectividade e o desempenho da rede em tempo real, utilizando SNMP como protocolo de coleta de métricas.

## :octicons-search-16: 2. Aplicações

### **Exemplo de Aplicação**

Este laboratório pode ser utilizado em diversos contextos acadêmicos e profissionais. Ele é útil para simular cenários reais de operação e monitoramento de redes, servindo como ambiente de validação de configurações e testes de interoperabilidade entre protocolos de roteamento e ferramentas de monitoramento.

**Possíveis Aplicações:**

* **Treinamento de equipes de NOC (Network Operations Center)**:
    Reproduz situações reais de conectividade entre roteadores Juniper, Huawei e Cisco em topologia em anel, utilizando OSPF e SNMP, permitindo que técnicos aprendam a detectar, analisar e resolver falhas.
* **Avaliação de interoperabilidade entre vendors**:
Permite testar como diferentes fabricantes interagem via OSPF, analisar convergência de rotas e identificar inconsistências na troca dinâmica de informações de roteamento.
* **Validação de templates SNMP no Zabbix**:
Ambiente controlado para validar, ajustar ou desenvolver templates de monitoramento SNMP para múltiplos fabricantes de roteadores, garantindo compatibilidade e precisão na coleta de métricas.
* **Ensino de protocolos de roteamento dinâmico**:
Proporciona aprendizado prático sobre configuração, manutenção e troca de rotas via OSPF em topologias ponto a ponto e em anel, incluindo análise de falhas e reconvergência.
  *	**Testes de monitoramento e descoberta automática**:
Permite avaliar a funcionalidade de descoberta automática de dispositivos via SNMP e o monitoramento de conectividade e desempenho em tempo real, simulando cenários variados de rede.
  *	**Simulação de políticas de rede e ACLs**:
Possibilita aplicar regras de filtragem de tráfego e verificar seu impacto sobre a comunicação e monitoramento, com análise de logs e traps SNMP no Zabbix.
---

## :material-tools: 3. Requisitos

Abaixo estão listados os requisitos mínimos de hardware e software necessários para executar o laboratório. Certifique-se de incluir as ferramentas essenciais, como **Containerlab** e **Docker**, além da rede `br-lab` previamente criada.
para saber mais sobre este itens acesse:

- [Criação da Rede br-lab](../../../../Ferramentas/Primeiros passos - preparando o ambiente.md)
-  <a target="_blank" href="https://www.docker.com/get-started/">Instalação do Docker</a>
-  <a target="_blank" href="https://containerlab.dev/install/">Instalação do containerlab</a>
- 
E tenha o zabbix previamente instalado, para saber mais sobre a instalação do zabbix acesse: [Instalação do Zabbix](../../../../Ferramentas/Zabbix/index.md)

### :material-alert: Tabela de Requisitos Minimos:

| Requisito           | Detalhes                |
| ------------------- |-------------------------|
| **CPUs**            | 4 vCPUs                 |
| **Memória RAM**     | 8 GB                    |
| **Espaço em Disco** | 10 GB (recomendado)     |
| **Containerlab**    | 0.45.0                  |
| **Docker Engine**   | 23.0.3                  |
| **Imagens**         | `vr-vjunos:23.2R1.14`, `vrnetlab/huawei_vrp:ne40e-8.180`, `xrd-control-plane:7.10.2` |
| **Rede Criada**     | `br-lab`                |


!!! warning "Atenção" 
    Verifique se o seu processador possui **suporte à virtualização por hardware** e se essa funcionalidade está **ativada na BIOS/UEFI**.  
    - Em processadores **Intel**, essa tecnologia é chamada de **VT-x** (Intel Virtualization Technology).  
    - Em processadores **AMD**, é conhecida como **AMD-V** (AMD Virtualization).  

    Sem essa funcionalidade ativada, as imagens como o **vJunos-router** não funcionarão corretamente.

---

## :fontawesome-solid-prescription-bottle: 4. Implantando o Lab

Aqui estão as instruções para **implantar o laboratório**. Você pode optar por uma **implantação pronta** ou uma **customizada**.

### :material-git: 4.1 Implantação Pronta

Este método permite ao usuário **baixar uma versão pré-montada** do laboratório, com a topologia e as configurações já definidas. Basta baixar o repositório e seguir para o início da execução.

!!! tip "Dica" 
    A implantação pronta é útil para quem deseja começar rapidamente com um ambiente configurado.

#### :octicons-download-16: Baixando o Lab

Para baixar o laboratório, execute o comando correspondente ao seu sistema operacional.

=== "Linux/Mac"

    ```bash
    curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/monitoramento-zabbix-multvendor/get.sh" && sh get.sh && cd monitoramento-zabbix-multvendor
    ```


=== "Windows"

    ```bash
    curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/monitoramento-zabbix-multvendor/get.bat" && call get.bat && cd monitoramento-zabbix-multvendor
    ```

Este comando fará o download do script de instalação e o direcionará para o diretório do laboratório.

!!! tip "Dica" 
    Antes de executar os scripts, verifique se as permissões de execução estão corretas (use `chmod +x get.sh` no Linux/Mac).

---

## :octicons-play-16: 5. Iniciando o Lab

Após o download ou personalização, siga as etapas abaixo para **iniciar o laboratório**.
Execute o comando abaixo dentro do diretório baixado.

```bash
sudo containerlab deploy

```

Esse comando iniciará a topologia definida no laboratório e criará todos os containers necessários.

!!! tip "Dica" 
    Caso ocorra algum erro, verifique a saída do comando para possíveis mensagens de erro. Use `docker logs <container_name>` para depurar.

---

## :material-access-point: 6. Acesso

Após o laboratório ser iniciado, você poderá acessar os dispositivos e serviços configurados na rede.

### :material-table: 6.1 Tabela de IPs e Portas de Serviço

Aqui está um exemplo de tabela de dispositivos, IPs e portas de serviço disponíveis no laboratório.

| Dispositivo         | IP de Acesso  | Porta   | Serviço           |
|---------------------|---------------|---------| ----------------- |
| **node1**           | 172.10.10.201 | 22      | SSH               |
| **node2**           | 172.10.10.202 | 22      | SSH               |
| **node3**           | 172.10.10.203 | 22      | SSH               |
| **Zabbix Server**   | 172.10.10.115 | 10051   | Zabbix Server     |
| **Zabbix Frontend** | 172.10.10.116 | 880/443 | Web UI (Zabbix)   |
| **Zabbix Agent**    | 172.10.10.117 | 10050   | Zabbix Agent      |
| **Zabbix Database** | 172.10.10.118 | 5432    | PostgreSQL        |
| **Graphite**        | 172.10.10.119 | 8080    | Web UI (Graphite) |


### :material-key-link: 6.2 Senhas de Acesso

| Serviço             | Usuário  | Senha            |
|---------------------|----------|------------------|
| **node1 (SSH)**     | `admin`  | `admin@123`      |
| **node2 (SSH)**     | `clab`   | `clab@123`       |
| **node3 (SSH)**     | `admin`  | `admin`          |
| **Zabbix (Web UI)** | `Admin`  | `zabbix`         |
| **Zabbix Database** | `zabbix` | `zabbixdatabase` |



!!! warning "Atenção" 
    antes de acessar, acesse o log de um dispositivo para verificar se ele foi iniciado e configurado corretamente.
---

## 7. :octicons-rocket-24: Próximos Passos

Ao iniciar o laboratório, o zabbix vai esta cru sem templates, para configura a descoberta automatica e os templates, acesse o [Configurando Auto Discovery](../../../../Ferramentas/Zabbix/Configurando%20Auto%20Discovery.md)

!!! warning "Atenção" 
    Atualmente a descoberta automatica só esta adicionando o template correto do juniper, para os outros fabricantes você deverar adicionar o template manualmente, 
---
