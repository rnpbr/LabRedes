### Estrutura dos Templates CLAB

Os templates CLAB seguem uma estrutura específica, que permite que o NetReplica interprete e aplique as configurações corretamente. Aqui está um exemplo de um template CLAB para um dispositivo ceos:

```yaml

  {{ name }}:
    kind: ceos
    image: ceos:latest
    {% if configuration_file is defined %}
    startup-config: {{ configuration_file }}
    {% endif %}
    {% if interface_map is defined %}
    binds:
        - {{ interface_map }}:/mnt/flash/EosIntfMapping.json:ro
    {% endif %}
    {% include 'clab/labels.j2' %}
```

Neste exemplo:

- `{{ name }}` é uma variável que será substituída pelo nome do dispositivo.
- `kind` define o tipo de dispositivo, neste caso, "ceos".
- `image` especifica a imagem do dispositivo.
- `startup-config` permite definir um arquivo de configuração inicial.
- `binds` permite mapear volumes, como o mapeamento de interfaces.
- `include` é usado para incluir labels adicionais do template CLAB.

### Criando Templates CLAB

Para criar seus próprios templates CLAB, siga a estrutura e o formato de exemplo fornecido. Você pode criar arquivos `.j2` lembrando que o nome do arquivo deverá ser o nome da plataforma, para cada tipo de dispositivo e personalizar as configurações conforme necessário. Salve seus templates no diretório `templates/clab/kinds/` do seu ambiente NetReplica.

Ao criar e usar templates CLAB, você tem flexibilidade para definir como os dispositivos serão provisionados e configurados dentro do ambiente CLAB, permitindo uma replicação precisa da sua rede.

Exemplo do template junos junos.j2

```yaml
{{ name }}:
            kind: crpd
            image: crpd:23.1R1.8
            {% if configuration_file is defined %}
            startup-config: {{ configuration_file }}
            {% endif %}
            {% if interface_map is defined %}
            binds:
                - {{ interface_map }}:/mnt/flash/EosIntfMapping.json:ro
            {% endif %}
            {% include 'clab/labels.j2' %}

```

## Passo2: Executando o NetReplica com o Arquivo de Configuração

---

Uma vez que você tenha criado e configurado o arquivo `.conf` com as opções desejadas, você está pronto para executar o NetReplica e iniciar a replicação e análise de redes com base nas informações do NetBox. Siga os passos abaixo para executar o NetReplica:

1. **Localização do Arquivo de Configuração**: Certifique-se de que o arquivo `.conf` esteja na localização correta. Se você estiver usando o NetReplica via Docker, lembre-se de que o arquivo `.conf` deve estar dentro do diretório "conf" que é criado após a execução do compose.
2. **Iniciando o NetReplica**: Abra um terminal ou prompt de comando e navegue até o diretório onde o NetReplica está instalado. Se você estiver usando o NetReplica via Docker, certifique-se de estar no diretório onde o arquivo `docker-compose.yml` está localizado.
3. **Executando o NetReplica**: Execute o comando para iniciar o NetReplica, passando o caminho para o arquivo `.conf` como um argumento. Por exemplo, se o arquivo `.conf` estiver no diretório atual e for chamado `netreplica.conf`, o comando pode ser:

    ```bash
    nrx -c <arquivo>.conf
    ```

   Se você estiver usando o NetReplica via Docker, o comando para executar pode ser:

    ```bash
    docker exec -it nrx ./nrx -c conf/<arquivo>.conf
    ```

4. **Acompanhando a Execução**: Durante a execução, o NetReplica irá usar as configurações do arquivo `.conf` para acessar o NetBox e iniciar a replicação e análise da rede. Acompanhe a saída do terminal para ver o progresso e qualquer mensagem relevante.
5. **Resultados da Execução**: Após a execução ser concluída, os resultados da replicação e análise estarão disponíveis no diretório de saída especificado no arquivo `.conf` (geralmente o diretório `OUTPUT_DIR`). Você poderá encontrar os arquivos exportados, como imagens, configurações de dispositivos e outros dados, de acordo com as configurações definidas.

Lembre-se de que o NetReplica é uma ferramenta poderosa para replicação e análise de redes com base nas informações do NetBox. Ao executar o NetReplica com o arquivo de configuração corretamente configurado, você estará explorando as capacidades de integração entre essas duas ferramentas para obter insights valiosos sobre sua rede.

## **Fontes**

1. NetReplica (NRX) GitHub Repository. Disponível em: **<a target="_blank" href="https://github.com/netreplica/nrx">https://github.com/netreplica/nrx</a>**
2. NetReplica Templates GitHub Repository. Disponível em: **<a target="_blank" href="https://github.com/netreplica/templates">https://github.com/netreplica/templates</a>**
3. ContainerLab Manual - Kinds. Disponível em: **<a target="_blank" href="https://containerlab.dev/manual/kinds/">https://containerlab.dev/manual/kinds/</a>**