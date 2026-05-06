# Guia: Deploy de Laboratórios de Rede usando VSCode e Containerlab

## Introdução

Este guia apresenta o processo de criação e deploy de laboratórios de rede utilizando o **Visual Studio Code (VSCode)** em conjunto com a extensão **Containerlab**.
O objetivo é demonstrar como essa integração pode **simplificar experimentos de rede**, aproximando a experiência de um ambiente real de produção.
Para profissionais de **infraestrutura**, o uso dessas ferramentas representa:

* **Maior previsibilidade** em mudanças de rede.
* **Agilidade** para criar e destruir ambientes de teste.
* **Menor risco operacional**, ao validar previamente cenários críticos.

---

## O que é o VSCode?

O **Visual Studio Code (VSCode)** é um editor de código leve e multiplataforma. Embora amplamente utilizado por desenvolvedores, ele também oferece recursos essenciais para administradores de sistemas e operadores de rede.
Com suporte a **extensões**, o VSCode pode ser transformado em uma **plataforma de gerenciamento centralizada**, onde você edita arquivos de configuração, conecta-se a servidores remotos, e agora, com o **Containerlab**, também gerencia laboratórios de rede completos.

---

## Benefícios para a Infraestrutura

### Produção

* Validação de alterações em ambientes isolados antes do deploy real.
* Testes de resiliência contra falhas de rede.
* Redução de tempo de troubleshooting.

### Pesquisa

* Criação de ambientes de teste controlados para simulação de protocolos.
* Reproduzir condições adversas (delay, jitter, perda de pacotes).
* Apoio a experimentos acadêmicos e artigos científicos.

### Operadores de Rede

* Menos dependência de linha de comando para tarefas comuns.
* Visualização gráfica da topologia.
* Integração com ferramentas de documentação (TopoView, Draw.io).

---

## Requisitos

Antes de iniciar, verifique:

* **VSCode instalado** em sua máquina.
* Leitura prévia da documentação do laboratório usado como exemplo:
  [Lab Monitoramento Zabbix](../../Laboratórios/Juniper/vJunos/Monitoramento-Zabbix/index.md).
* Familiaridade básica com a interface do VSCode:
  [Introdução ao VSCode](index.md).

---

## Uso remoto com SSH

Se você pretende executar o VSCode em um **host remoto** (ex.: servidor ou VM de testes):

* Primeiro, instale a extensão **Remote SSH**. Ela permite que o VSCode acesse arquivos e recursos do servidor remoto como se estivessem locais.
* Após se conectar ao host remoto, prossiga com a instalação das demais extensões e configuração do ambiente.

Isso é útil em ambientes de laboratório ou produção onde os recursos de hardware para containers não estão disponíveis na sua máquina pessoal.

![SSH Mode](../../../img/vscode/2-ssh-mode.png)

---

## 1. Instalação da extensão Containerlab

A primeira etapa é instalar a extensão **Containerlab** no VSCode.
Essa extensão adiciona um painel lateral onde é possível:

* Criar, destruir e editar laboratórios.
* Visualizar topologias de forma gráfica.
* Monitorar logs e status dos nós.

![Install](../../../img/vscode/1-install.png)

---

## 1.1 Instalação do EdgeShark

O **EdgeShark** é uma integração que permite abrir capturas de tráfego diretamente no VSCode, sem depender do Wireshark externo.
Isso simplifica a análise de pacotes nos experimentos de rede, tornando o VSCode uma ferramenta completa para experimentação.

Para instalar:

* Abra a barra de pesquisa superior do VSCode.
* Digite:

  ```
  >containerlab: install Edgeshark
  ```
* Pressione Enter.

![EdgeShark](../../../img/vscode/1.1-edgeshark.png)

---

## 2. Deploy de um Laboratório

Nesta seção, vamos fazer o **deploy do laboratório de monitoramento Zabbix**.

1. Abra a aba lateral do Containerlab no VSCode.
2. Clique em **Open Folder** e escolha a pasta de trabalho.
3. No terminal integrado, baixe o laboratório de exemplo com os comandos abaixo:

=== "Linux/Mac"

```bash
curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/zabbix-lab/get.sh?ref_type=heads&inline=false" && sh get.sh && cd zabbix-lab
```

=== "Windows"

```bash
curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/zabbix-lab/get.bat?ref_type=heads&inline=false" && call get.bat && cd zabbix-lab
```

Esse comando baixa um script de instalação, executa-o e cria a pasta com o laboratório.

Após a conclusão, o laboratório aparecerá na aba **Local Labs**. Basta clicar com o botão direito no laboratório e escolher **Deploy**.

![Deploy](../../../img/vscode/6-Deploy.gif)

---

## 3. Funcionalidades Principais

### Visualização e edição

No **TopoView**, a topologia é exibida de forma gráfica, permitindo:

* Adicionar ou remover nós e links.
* Alterar interfaces, endereçamento IP e limitações de desempenho.
* Associar arquivos de configuração diretamente a cada nó.
* Editar o arquivo `.clab` manualmente, caso prefira.

Isso substitui edições manuais demoradas em YAML, dando maior agilidade ao processo.

---

### Monitoramento de nós e logs

Cada nó da topologia pode ser inspecionado diretamente no VSCode. É possível abrir **logs em tempo real**, o que ajuda no diagnóstico de falhas e validação de funcionamento de serviços.

![Logs](../../../img/vscode/7-Logs.gif)

---

### Captura e análise de tráfego

Com o **EdgeShark**, é possível capturar pacotes de interfaces específicas dentro da topologia.
Essa funcionalidade é equivalente ao uso do Wireshark em um ambiente real, sendo ideal para análise de protocolos e troubleshooting.

![SSH Wireshark](../../../img/vscode/8-ssh-wireshark.gif)

---

### Simulação de falhas (Link Impairment)

O recurso **Link Impairment** permite adicionar condições adversas à rede simulada:

![Link Imparciment](../../../img/vscode/9-Link-imparciment.gif)

* **Delay (ms)** – tempo de resposta.
* **Jitter** – variação do delay.
* **Loss (%)** – perda de pacotes.
* **Rate-limit (Mbps)** – limitação de banda.
* **Corrupt (%)** – corrupção de pacotes.

Esse tipo de simulação é muito valioso para avaliar como sistemas de produção se comportariam em cenários de instabilidade.


---

### Outras opções úteis

Na aba de gerenciamento, encontramos funcionalidades adicionais:

1. **Destroy (cleanup)** – remove o laboratório e todos os dados persistentes.
2. **Redeploy (cleanup)** – reinicia o lab do zero.
3. **Save config** – salva a configuração atual dos nós.
4. **Inspect** – mostra informações de imagem e rede.
5. **SSH (all nodes)** – abre sessões SSH para todos os nós.
6. **Graph (draw.io)** – exporta a topologia para documentação.
7. **Graph (TopoView)** – abre a topologia no visualizador gráfico.
8. **Edit topology** – edição manual da topologia `.clab`.

![Lab Options](../../../img/vscode/10-lab-options.png)

Essas funções complementam o ciclo de vida de um laboratório de rede, desde a criação até o descarte e documentação.

---

## 4. Próximos Passos

Após dominar as funcionalidades básicas, recomenda-se:

* Fazer deploy de outros labs disponiveis [aqui](../../Laboratórios/index.md)