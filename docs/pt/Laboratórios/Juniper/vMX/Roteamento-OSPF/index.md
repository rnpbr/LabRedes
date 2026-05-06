# Roteamento OSPF

## :material-bookmark: **Introdução**

Este laboratório simula uma rede com 3 roteadores em uma topologia em anel, configurados utilizando OSPF para roteamento dinâmico e SNMP para envio de telemetria pela rede.

## :material-lan: **1. Topologia e Configurações**

A topologia consiste em três roteadores (PB, PE, JPA) conectados em um anel. Cada roteador está configurado com interfaces de rede e endereços IP, além de protocolos OSPF para roteamento e SNMP para monitoramento, como podemos ver na imagem a seguir.

![Topologia.png](../../../../../img/labs_imgs/Topologia_ospf_lab.png)

Os roteadores estão configurados com as seguintes tecnologias:

- **OSPF (Open Shortest Path First)**: Utilizado para roteamento dinâmico na rede, permitindo que os roteadores troquem informações sobre rotas e atualizações de topologia.
- **SNMP (Simple Network Management Protocol)**: Utilizado para monitoramento e gerenciamento da rede, permitindo o acesso a informações de telemetria dos dispositivos.

## :material-tools: **2. Instalação**
### :material-alert: 2.1 Pré requisitos:

Para iniciar o laboratório, é necessário a instalação e configuração dos seguintes componentes:

- Netbox
- Netreplica
- Containerlab

Caso o seu ambiente não esteja configurado, siga os passos [Guia de Configuração](../../../../../Getting%20Started.md)

   
### :material-application-import: 2.2 Importando Template no Netbox:
O Containerlab utiliza <a target="_blank" href="https://containerlab.dev/manual/nodes/#remote-startup-config ">startup-config</a> para importar configurações aos equipamentos, essas definidas em templates dentro do Netbox.

1. :material-git: **No Netbox, crie um Data source e adicione o repositório do git abaixo:** 
```bash
https://git.rnp.br/gci/dev/inovacao-ciberinfraestrutura/config-templates-data-source
```
Como adicionar: [Render Templates - #Templates remotos](../../Guias/Netbox/Render_Templates/index.md/#11-templates-remotos)

2. **Importe o template do laboratório de OSPF:**
     1. Acesse seu Netbox e vá em **Provisionamento** > **Modelos de Configuração**.
     2. Crie um template e defina um nome de sua escolha.
     3. Em **Data Source** escolha o nome do data source criado no passo **1**.
     4. Em **File** Selecione: ```Juniper/<imagem>/OSPF.jinja2```]
   
    !!! warning "Atenção"
        Atente-se a imagem do dispositivo, pois os templates de configuração são criados de maneiras distintas para cada tipo de imagem

3. :material-link-variant: **Associando Templates aos Dispositivos:**
      1. No seu Netbox, acesse **Dispositivos > Dispositivos**.
      2. Selecione o dispositivo que deseja associar ao template e clique em **editar**. 
      3. Na categoria Gestão, em **Modelo de configuração** selecione o nome do template definido no passo **2.2**.
      4. Salve as alterações.


### :material-laptop: 2.3 **Montando o Laboratório:**
Agora, com o Netreplica iremos puxar as informações do Netbox para montar 
o arquivo `.clab` que será utilizado pelo Containerlab para subir o laboratório. 

1. Na pasta onde o container do Netreplica está, dê o seguinte comando para importar as configurações do Netbox: 
```bash
nrx -c conf/<arquivo>.conf -n ospf-lab
```
2. Agora com o arquivo `.clab` criado, utilize o comando para subir o laboratório:
```bash
sudo -E clab dep -t conf/lab/ospf-lab.clab.yaml
```
!!! warning "Atenção"
    Os dispositivos necessitam de um tempo para serem incializados e configurados, pode ser que o laboratório (graphite) já esteja disponível e você não consiga acessar os dispositivos. </br>
!!! info "Dica"
    Para visualizar os logs do container e verificar se já foi configurado, você pode usar:
    ```bash
    docker logs <nome_do_container> -f
    ```

## **3. Acesso**

Existem duas formas de acesso aos dispositivos na rede:

- **Acesso via SSH aos roteadores**: Utilize um cliente SSH para se conectar aos roteadores utilizando o endereço IP de cada dispositivo ou o nome atribuído pelo Containerlab, juntamente com as credenciais de login fornecidas. O endereço IP de gerência de cada roteador é exibido após a execução do laboratório pelo Containerlab.

    Exemplo:

    ```bash
    
    ssh admin@<endereço_IP_do_roteador>
    ```

    ou

    ```bash
    
    ssh admin@<nome_do_roteador>
    ```

- **Acesso ao Graphite (Servidor de Tepologia)**: Acesse o Graphite através do navegador utilizando o endereço IP e a porta configurados. Você também pode acessar diretamente clicando no ícone de SSH no roteador desejado.

    URL: **`http://<endereço_IP_do_Graphite>:8080/graphite/`**

    Credenciais:

  - Usuário: admin
  - Senha: admin@123

## **4. Monitoramento**

Para monitorar a rede e os dispositivos, você pode utilizar ferramentas como edgeshark para análise de pacotes ou ferramentas de monitoramento SNMP.

- **edgeshark**: Capture e analise o tráfego de rede para diagnóstico de problemas e monitoramento de desempenho.
- **Monitoramento SNMP**: Utilize ferramentas compatíveis com SNMP para monitorar métricas de desempenho e saúde da rede.
