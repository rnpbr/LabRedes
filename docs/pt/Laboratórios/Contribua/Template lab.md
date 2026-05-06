# Template lab (Nome Do lab)

Este template serve como um **exemplo** para a criação de guias de implementação de laboratórios no Containerlab. Ele está estruturado de forma a servir como modelo para todos os laboratórios do projeto, com informações que devem ser seguidas de maneira consistente em cada documentação. Cada laboratório pode ter suas especificidades, mas a estrutura geral e as seções a seguir permanecem iguais para todos os labs.

---

## 1. Descrição

### **Objetivo do Lab**

Descreva o objetivo do laboratório de forma clara, explicando o que será demonstrado ou testado. Seja breve, mas inclua as funcionalidades principais que o usuário irá explorar.

Nesta parte deve conter uma imagem contendo a topologia do lab
[Topologia do Lab](../../../img/labs_imgs/Topologia_ospf_lab.png)

**Exemplo:O laboratório "ospf-lab" demonstra a configuração e teste de roteamento OSPF (Open Shortest Path First) em uma rede composta por múltiplos roteadores. O foco principal é verificar o estabelecimento da vizinhança OSPF e o roteamento entre os dispositivos da rede.**

!!! tip "Dica" 
    Mantenha a descrição clara e concisa, destacando o que é essencial para o usuário entender rapidamente o que o laboratório irá proporcionar.

**Topologia do Lab**
Aqui, inclua o diagrama ou uma descrição textual detalhada da topologia, mencionando os dispositivos e como estão interligados.

---

Claro! Abaixo está um **template geral da seção "Exemplo de Aplicação"**, com uma **descrição orientativa** para o usuário entender o que incluir nessa parte do guia, seguida por um **exemplo prático** que pode ser adaptado em qualquer laboratório semelhante:

---

### **Exemplo de Aplicação**

**Descrição:**
Utilize esta seção para apresentar cenários práticos e objetivos nos quais o laboratório pode ser aplicado. O foco deve estar nas possíveis finalidades de uso, como treinamento, testes de desempenho, validação de configurações ou estudo de protocolos. Evite detalhes técnicos da implementação e concentre-se em **para que** o laboratório pode ser usado em ambientes reais ou acadêmicos.

**Exemplo de Aplicação:**

Este laboratório é ideal para cenários de simulação de redes reais, especialmente no contexto de roteamento dinâmico e monitoramento. Ele pode ser aplicado em:

* **Capacitação técnica**: Treinamento de profissionais em protocolos de roteamento (como OSPF) e monitoramento com SNMP, utilizando ferramentas como o Zabbix.
* **Testes de ambientes monitorados**: Avaliação de como roteadores se comportam sob monitoramento contínuo e descoberta automática de dispositivos.
* **Ensino em disciplinas de redes**: Ambiente de apoio a aulas práticas de redes de computadores, com foco em topologias ponto a ponto e integração com sistemas de gestão de rede.
* **Validação de integração de ferramentas**: Utilizado para validar a comunicação entre roteadores e plataformas de monitoramento em ambientes virtualizados.

---

## 3. Requisitos

Este tópico deve listar **os requisitos mínimos de hardware e software** necessários para executar o laboratório. Certifique-se de incluir as ferramentas essenciais, como **Containerlab** e **Docker**, além da rede `br-lab`.

### Exemplo de Tabela de Requisitos:

| Requisito           | Detalhes |
|---------------------| --- |
| **CPUs**            | [x] CPUs (especificar) |
| **Memória RAM**     | [x] GB |
| **Espaço em Disco** | [x] GB |
| **Containerlab**    | [Versão do Containerlab] |
| **Rede Criada**     | [ br-lab] |

!!! tip "Dica" 
    Verifique se a versão do Docker e do Containerlab são compatíveis para evitar erros durante a implantação.

---

## 4. Implantando o Lab

Este tópico descreve o processo de **implantação do laboratório**, com as instruções detalhadas para o usuário baixar e iniciar o ambiente.

### 4.1 Implantação Pronta

Este método permite ao usuário **baixar uma versão pré-montada** do laboratório, com a topologia e as configurações já definidas. Basta baixar o repositório e seguir para o início da execução.

!!! tip "Dica" 
    A implantação pronta é útil para quem deseja começar rapidamente com um ambiente configurado, mas não permite modificações na topologia inicial.

### Baixando o Lab

Para baixar o laboratório, execute o comando correspondente ao seu sistema operacional.

=== "Linux/Mac"

    ```bash
    curl -L -o get.sh "<https://git.rnp.br/redes-abertas/labs/-/raw/main/><nome-do-lab>/get.sh?inline=false" && sh get.sh && cd <nome-do-lab>
    
    ```

=== "Windows"

    ```bash
    curl -L -o get.bat "<https://git.rnp.br/redes-abertas/labs/-/raw/main/><nome-do-lab>/get.bat?inline=false" && call get.bat && cd <nome-do-lab>
    
    ```

Este comando fará o download do script de instalação e o direcionará para o diretório do laboratório.

!!! tip "Dica" 
    Antes de executar os scripts, verifique se as permissões de execução estão corretas (use `chmod +x get.sh` no Linux/Mac).

---

### 4.2 Implantação Customizada (Em Desenvolvimento)

Se você deseja uma **versão personalizada** do laboratório, pode começar a modificação utilizando ferramentas como **NetBox** e **NetReplica**. **Este passo está em desenvolvimento**, mas logo teremos mais informações.

!!! tip "Dica" 
    A personalização avançada pode ser útil para ajustar a topologia às suas necessidades específicas, como incluir mais dispositivos ou testar diferentes cenários.

---

## 5. Iniciando o Lab

Após o download ou personalização, siga as etapas abaixo para **iniciar o laboratório**.

### 5.1 Subindo o Lab

Execute o comando abaixo dentro do diretório onde o laboratório foi baixado ou personalizado:

```bash
sudo containerlab deploy

```

Esse comando iniciará a topologia definida no laboratório e criará todos os containers necessários.

!!! tip "Dica" 
    Caso ocorra algum erro, verifique a saída do comando para possíveis mensagens de erro. Use `docker logs <container_name>` para depurar.

---

## 6. Acesso

Após o laboratório ser iniciado, você poderá acessar os dispositivos e serviços configurados na rede.

### 6.1 Tabela de IPs e Portas de Serviço

Aqui está um exemplo de tabela de dispositivos, IPs e portas de serviço disponíveis no laboratório.

| Dispositivo | IP de Acesso | Porta | Serviço |
| --- | --- | --- | --- |
| **Roteador 1** | 192.168.1.1 | 22 | SSH |
| **Roteador 2** | 192.168.1.2 | 22 | SSH |
| **Servidor de Monitoramento** | 192.168.1.3 | 8080 | Web (Graphite) |
| **Servidor DB** | 192.168.1.4 | 3306 | MySQL |

### 6.2 Senhas de Acesso

Aqui está um exemplo de tabela com as senhas de acesso dos serviços configurados no laboratório.

| Serviço | Usuário | Senha |
| --- | --- | --- |
| **Roteador 1 (SSH)** | admin | admin@123 |
| **Roteador 2 (SSH)** | admin | admin@123 |
| **Graphite (Web)** | admin | admin@123 |
| **Banco de Dados MySQL** | root | mysql@123 |

!!! warning "Atenção" 
    antes de acessar acesse o log de um dispositivo para verificar se ele foi iniciado e configurado corretamente.
---

## 7. :octicons-rocket-24: Próximos Passos

esta parte destina-se para o que fazer depois de ter iniciado o laboratório. vc pode adicionar outros guias aqui como de 
uso de alguma ferramenta ou operação do laboratorio 
---

### Conclusão (Apagar depois)

Este template foi projetado para servir como **estrutura padrão** para documentação de todos os laboratórios do projeto. Ele deve ser seguido de maneira consistente para garantir clareza e padronização na criação de novos laboratórios. As seções descritas são essenciais e aplicáveis a qualquer laboratório dentro do Containerlab, com o objetivo de proporcionar uma experiência fluida tanto para os desenvolvedores quanto para os usuários.