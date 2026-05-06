## Introdução

Este laboratório oferece uma abordagem prática para configurar dispositivos de rede utilizando o protocolo NETCONF e modelos de dados YANG. 

### Pré-requisitos

- containerlab
- `uv` (caso queira criar manualmente o ambiente virtual, utilize Python 3.12)

Para iniciar, clone o repositório contendo scripts e exemplos em:
```
ssh://git@git.rnp.br:2022/redes-abertas/schema-driven-cfg.git
```  
## Construindo o Ambiente de Teste com `containerlab`

Nesta seção, utilizaremos o `containerlab` para implantar uma topologia de rede simples definida no arquivo `simple-lab.yaml`.

1.  **Geração de Imagens (se necessário):**
    As imagens dos roteadores virtuais (vSRX para Juniper e NE40E para Huawei) precisam estar disponíveis localmente. Utilize o `vrnetlab` para construir essas imagens. Consulte a <a target="_blank" href="https://containerlab.dev/manual/vrnetlab/#vrnetlab">documentação do `vrnetlab`</a> para instruções detalhadas sobre como gerar as imagens `VSRX 20.1R1.13` e `Huawei NE40E V800R011C00SPC607B607`. A imagem Cisco XRd não precisa ser gerada dessa maneira, pois já é um container, basta seguir as instruções no site do containerlab.

2.  **Implantação da Topologia:**
    Com as imagens prontas, execute o seguinte comando para iniciar o laboratório:

    ```bash
    sudo containerlab deploy -t simple-lab.yaml
    ```
    O `containerlab` provisionará os contêineres e exibirá uma tabela com os endereços IP para cada dispositivo. Anote esses IPs, pois serão utilizados nas etapas subsequentes.

## Instalando Dependências Python

Os scripts Python utilizados neste laboratório possuem dependências externas. Siga um dos métodos abaixo para instalá-las:

#### Usando `uv` (Recomendado)

Se você possui o `uv` instalado, execute o comando abaixo na raiz do repositório clonado para criar um ambiente virtual e instalar as dependências:

```bash
uv sync
```
Em seguida, ative o ambiente virtual:
```bash
source .venv/bin/activate
```

#### Usando `pip` com um Ambiente Virtual Manual

Se preferir gerenciar o ambiente virtual manualmente com Python 3.12+ e `pip`:

1.  Crie um ambiente virtual:
    ```bash
    python3 -m venv .venv
    ```
2.  Ative o ambiente virtual:
    ```bash
    source .venv/bin/activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Testando Operações NETCONF

Com o ambiente configurado, podemos testar as operações NETCONF usando o script `netconf_test.py`. Este script utiliza arquivos de configuração YAML para definir os parâmetros de conexão do dispositivo e payloads XML para as operações NETCONF.

1.  **Atualize os Arquivos de Configuração do Dispositivo:**
    Modifique os arquivos `huawei_device_config.yaml`, `junos_device_config.yaml` e `cisco_device_config.yaml` com os endereços IP corretos dos seus dispositivos (fornecidos pelo `containerlab`) e as credenciais correspondentes.

    Exemplo (`huawei_device_config.yaml`):
    ```yaml
    # filepath: huawei_device_config.yaml
    device:
    hostname: "172.20.20.5"
    username: "admin"
    password: "admin"
    port: 830
    type: "huaweiyang"
    ```

2.  **Execute o Script `netconf_test.py`:**

    **Uso do Script:**
    ```bash
    python netconf_test.py -c <arquivo_config_yaml> -p <arquivo_payload_xml>
    ```

    **Argumentos:**
    -   `-c CONFIG`, `--config CONFIG`: Caminho para o arquivo de configuração YAML do dispositivo (e.g., `huawei_device_config.yaml`).
    -   `-p PAYLOAD`, `--payload PAYLOAD`: Caminho para o arquivo XML contendo o payload NETCONF (e.g., `xml/huawei-native-interface-ip.xml`).

    **Exemplo de Aplicação de Configuração de Interface em um Dispositivo Huawei:**
    ```bash
    python netconf_test.py -c huawei_device_config.yaml -p xml/huawei-native-interface-ip.xml
    ```
    Acesse o dispositivo e verifique que o IP `10.1.1.2/24` foi configurado na interface `Ethernet1/0/1`.

    Para remover a configuração utilize o payload de deleção:
    ```bash
    python netconf_test.py -c huawei_device_config.yaml -p xml/huawei-native-interface-ip-delete.xml
    ```

    **Exemplo de Aplicação de Configuração de Interface em um Dispositivo Juniper:**
    ```bash
    python netconf_test.py -c junos_device_config.yaml -p xml/junos-native-interface-ip.xml
    ```
    Acesse o dispositivo e verifique que o IP `10.1.1.2/24` foi configurado na interface `ge-0/0/0`.

    Para remover a configuração utilize o payload de deleção:
    ```bash
    python netconf_test.py -c junos_device_config.yaml -p xml/junos-native-interface-ip-delete.xml
    ```

    **Exemplo de Aplicação de Configuração de Interface em um Dispositivo Cisco:**
    ```bash
    python netconf_test.py -c cisco_device_config.yaml -p xml/cisco-native-interface-ip.xml
    ```
    Acesse o dispositivo e verifique que o IP `192.168.1.12` foi configurado na interface `GigabitEthernet0/0/0/0`.

    Para remover a configuração utilize o payload de deleção:
    ```bash
    python netconf_test.py -c cisco_device_config.yaml -p xml/cisco-native-interface-ip-delete.xml
    ```

    **Exemplo com o uso de modelos OpenConfig:**

    Agora tente realizar a mesma operação utilizando os payloads do modelo OpenConfig:
    ```bash
    #Huawei
    python netconf_test.py -c huawei_device_config.yaml -p xml/openconfig-huawei-interface-ip.xml
    #Juniper
    python netconf_test.py -c junos_device_config.yaml -p xml/openconfig-junos-interface-ip.xml
    ```


## Obtendo Modelos YANG dos Dispositivos


Os modelos YANG definem a estrutura dos dados de configuração e estado dos dispositivos de rede, servindo como base para automação e interoperabilidade via NETCONF. Compreender e explorar esses modelos é fundamental para criar payloads NETCONF corretos.

A seguir, apresentamos métodos para obter os modelos YANG dos dispositivos Huawei, Juniper e Cisco deste exemplo.

### Obtendo Modelos YANG de Dispositivos Huawei

No caso de dispositivos Huawei, podemos obter os modelos YANG via NETCONF, sem necessidade de alterar a configuração inicial do dispositivo feita pelo containerlab. Utilize o script `huawei_get_schema.py` para baixar os modelos para uma pasta local.

**Uso do Script:**

```bash
python huawei_get_schema.py <host> <username> <password> [output_dir]
```

**Argumentos:**

-   `host`: Endereço IP ou hostname do dispositivo Huawei (obtido do `containerlab`).
-   `username`: Nome de usuário para autenticação NETCONF.
-   `password`: Senha para autenticação NETCONF.
-   `output_dir` (Opcional): Diretório para salvar os arquivos YANG. Padrão: `huawei-schema`.


### Obtendo Modelos YANG de Dispositivos Juniper

Para dispositivos Juniper (Junos OS), recomenda-se obter os modelos YANG diretamente pela CLI do equipamento e transferi-los para sua máquina local.

Consulte a <a target="_blank" href="https://www.juniper.net/documentation/us/en/software/junos/netconf/topics/task/netconf-yang-module-obtaining-and-importing.html">documentação oficial da Juniper</a> para orientações detalhadas.

## Obtendo o modelo YANG de dispositivos Cisco

Para obter o modelo YANG de um dispositivo Cisco, execute o script `cisco_get_schema.py` da seguinte maneira:
```
usage: cisco_get_schema.py [-h] [--port PORT] host username password [output_dir]
argumentos:
  host          Endereço IP ou hostname do dispositivo Cisco
  username      Nome de usuário para autenticação no dispositivo
  password      Senha para autenticação no dispositivo
  output_dir    (Opcional) Caminho para o diretório onde os arquivos YANG serão salvos - default=cisco-schema
  --port        (Opcional) Porta NETCONF - default=830
ex:
python cisco_get_schema.py 192.168.1.2 admin 'senha' cisco-schema --port 830
```

Os arquivos YANG serão baixados e salvos no diretório especificado (quando disponível, o nome seguirá o padrão `<modulo>@<revision>.yang`).
