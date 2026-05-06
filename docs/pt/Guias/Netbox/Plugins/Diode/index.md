# :material-power-plug-outline: Diode Plugin

O plugin Diode para o NetBox é uma solução poderosa para quem deseja automatizar a descoberta e a ingestão de dados de dispositivos de rede. Com ele, o NetBox passa a receber informações de forma dinâmica por meio de agentes ou scripts personalizados, que realizam a coleta, o tratamento e a inserção dos dados diretamente no sistema. Essa funcionalidade facilita a integração com ambientes complexos e promove uma documentação contínua e automatizada da infraestrutura de rede.

## :simple-git: **Repositório do Plugin**
Copie o link abaixo ou clique a seguir para acessar o <a target="_blank" href="https://github.com/netboxlabs/diode/tree/develop">Repositório do Github</a>

```
https://github.com/netboxlabs/diode/tree/develop
```

---

## :material-receipt-text-edit-outline: **1. Componentes**
O Diode é composto por três componentes principais, que trabalham em conjunto para realizar a ingestão automatizada de dados no NetBox:

1. **Plugin Diode para NetBox:** Responsável pela integração com o ORM do NetBox e pela gestão de chaves de API, permitindo que o NetBox aceite dados externos de forma segura e estruturada. [Instalando o Diode Plugin](./Instalando%20o%20Diode%20Plugin.md)

2. **Servidor Diode (Diode Server):** Atua como o núcleo do serviço, processando os dados recebidos e realizando a conciliação (reconciliation) com as informações existentes no NetBox. Veja aqui como instalar [Instalando o Diode Server](./Instalando%20o%20Diode%20Server.md)

3. **Diode Client:** Implementado como um SDK em Python, este componente coleta os dados dos dispositivos e os envia ao servidor via gRPC/protobuf. Pode ser facilmente incorporado a scripts personalizados ou integrações existentes. Veja aqui como instalar [Instalando o Diode Client](./Instalando%20o%20Diode%20Client.md)

!!! tip "Dica" 
    Os números dos componentes indicam a **ordem de instalação**, siga-os para ter uma melhor experiência e entendimento do assunto.

---

## :fontawesome-solid-building-columns: **2. Arquitetura**
Para facilitar a compreensão do funcionamento do Diode, o diagrama abaixo ilustra a arquitetura dos seus principais componentes e como eles se comunicam entre si:


