# :material-bookmark: Juniper Vjunos Monitoramento Zabbix

Este laboratório simula, via Containerlab, a interligação entre dois roteadores representando a conexão BA–ES na RNP, com monitoramento via Zabbix e SNMPv2.

---

## :material-bookmark: 1. Descrição

### :octicons-goal-16: 1.1 Objetivo do Lab

O laboratório “zabbix-rnp-lab” demonstra a simulação da conexão entre dois roteadores representando a interligação entre BA e ES no backbone da RNP, utilizando o Containerlab. O roteamento entre os dispositivos é realizado por meio do protocolo OSPF, garantindo a troca dinâmica de rotas. O foco principal é integrar essa topologia ao Zabbix via SNMPv2, possibilitando o monitoramento em tempo real. Além disso, o laboratório destaca a funcionalidade de descoberta automática de dispositivos na rede.

### :material-lan: 1.2 Topologia do Lab

![Topologia do Lab](../../../../../img/labs_imgs/Topologia_Zabbix.svg)


A topologia deste laboratório é composta por dois roteadores interligados por uma rede ponto a ponto /31, permitindo a comunicação direta entre eles. Os roteadores estão configurados com OSPF para garantir o roteamento dinâmico entre as interfaces. O monitoramento da rede é feito por meio de uma rede externa chamada br-lab, onde os roteadores estão conectados por interfaces virtuais. Através dessa configuração, o Zabbix é capaz de monitorar a conectividade e o desempenho da rede, 

---

## :octicons-search-16: 2. Aplicações

### **Exemplo de Aplicação**

Este laboratório pode ser utilizado em diversos contextos acadêmicos e profissionais. Ele é útil para simular cenários reais de operação e monitoramento de redes, servindo como ambiente de validação de configurações e testes de interoperabilidade entre protocolos de roteamento e ferramentas de monitoramento.

**Possíveis Aplicações:**

* **Treinamento de equipes de NOC (Network Operations Center)**: Reproduz situações reais de conectividade entre roteadores com OSPF e monitoramento via SNMP para familiarizar técnicos com detecção e análise de falhas.
* **Avaliação de desempenho da descoberta automática via SNMP**: Permite testar o funcionamento da descoberta de hosts em diferentes condições de rede e topologia.
* **Validação de templates SNMP no Zabbix**: Pode ser usado para validar ou desenvolver templates de monitoramento SNMP para roteadores em ambientes controlados.
* **Ensino de protocolos de roteamento dinâmico**: Proporciona um ambiente de aprendizado prático sobre configuração e troca de rotas via OSPF em redes ponto a ponto.

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

| Requisito           | Detalhes                                                                 |
| ------------------- | ------------------------------------------------------------------------ |
| **CPUs**            | 4 vCPUs                                                                  |
| **Memória RAM**     | 8 GB                                                                     |
| **Espaço em Disco** | 10 GB (recomendado)                                                      |
| **Containerlab**    | 0.45.0                                                                   |
| **Docker Engine**   | 23.0.3                                                                   |
| **Imagens**         | `vr-vjunos:23.2R1.14`                                                    |
| **Rede Criada**     | `br-lab`                                                                 |


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
    curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/zabbix-lab/get.sh?ref_type=heads&inline=false" && sh get.sh && cd zabbix-lab
    ```


=== "Windows"

    ```bash
    curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/zabbix-lab/get.bat?ref_type=heads&inline=false" && call get.bat && cd zabbix-lab
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

| Dispositivo           | IP de Acesso  | Porta   | Serviço           |
| --------------------- | ------------- |---------| ----------------- |
| **Roteador BA**       | 172.10.10.6   | 22      | SSH               |
| **Roteador ES**       | 172.10.10.11  | 22      | SSH               |
| **Zabbix Server**     | 172.10.10.115 | 10051   | Zabbix Server     |
| **Zabbix Frontend**   | 172.10.10.116 | 880/443 | Web UI (Zabbix)   |
| **Zabbix Agent**      | 172.10.10.117 | 10050   | Zabbix Agent      |
| **Zabbix Database**   | 172.10.10.118 | 5432    | PostgreSQL        |
| **Graphite** | 172.10.10.119 | 8080    | Web UI (Graphite) |


### :material-key-link: 6.2 Senhas de Acesso

| Serviço               | Usuário  | Senha            |
| --------------------- | -------- | ---------------- |
| **Roteador BA (SSH)** | `admin`  | `admin@123`      |
| **Roteador ES (SSH)** | `admin`  | `admin@123`      |
| **Zabbix (Web UI)**   | `Admin`  | `zabbix`         |
| **Zabbix Database**   | `zabbix` | `zabbixdatabase` |



!!! warning "Atenção" 
    antes de acessar, acesse o log de um dispositivo para verificar se ele foi iniciado e configurado corretamente.
---

## 7. :octicons-rocket-24: Próximos Passos

Ao iniciar o laboratório, o zabbix vai esta cru sem templates, para configura a descoberta automatica e os templates, acesse o [Configurando Auto Discovery](../../../../Ferramentas/Zabbix/Configurando%20Auto%20Discovery.md)

---
