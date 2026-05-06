# Netbox

## 1.Instalação do Netbox e importações

NetBox é uma aplicação web open source para gerenciamento de infraestrutura de redes e data centers. Ele permite documentar dispositivos, racks, conexões, endereços IP, circuitos, entre outros recursos, facilitando o controle e a automação do ambiente de TI.

### 1.1 Pré-requisitos

* **Docker** instalado → <a href="https://docs.docker.com/get-docker/" target="_blank">Guia oficial</a>
* **Docker Compose** instalado → <a href="https://docs.docker.com/compose/install/" target="_blank">Guia oficial</a>
* 
* Acesso a **Git** para clonar repositórios.

> **Nota:** Este procedimento é indicado para ambientes de teste ou homologação. Para produção, revise as configurações de segurança antes da publicação.

### 1.2 Clonar o repositório oficial

```bash
git clone https://github.com/netbox-community/netbox-docker.git
cd netbox-docker
```


### 1.3 Configuração de Variáveis de Ambiente

O repositório possui arquivos `.env` de exemplo.

1. Acesse a pasta `env/`:

   ```bash
   cd env
   ```
2. edite os arquivos conforme necessário:

   * `netbox.env` → Configurações do NetBox (e-mail, secret key, idioma, timezone).
   * `postgres.env` → Credenciais do banco de dados.
   * `redis-cache.env` → Credencias do Redis.
   * `redis.env` → Credencias do Redis.

> **Recomendação:**
> Mesmo para ambientes de teste, altere senhas padrão e credenciais antes de colocar em produção.


### 1.4 Alterar a versão do NetBox (opcional)

Para mudar a versão:

* Edite o `docker-compose.yml` ou `docker-compose.override.yml` e ajuste a imagem:

  ```yaml
  image: netboxcommunity/netbox:<versão>
  ```
* Consulte as versões compatíveis em: <a target="_blank" href="https://github.com/netbox-community/netbox-docker/releases">Releases Netbox Docker</a>

> **Atenção:** Alterações entre versões muito distantes podem exigir ajustes no banco de dados ou configurações.


### 1.5 Configuração de Porta (opcional)

Crie o arquivo `docker-compose.override.yml` para expor uma porta específica:

```bash
tee docker-compose.override.yml <<EOF
version: '3.4'
services:
  netbox:
    ports:
      - 8000:8080
EOF
```

> Troque `8000` se a porta estiver em uso (ex.: `8080` ou `8081`).


### 1.6 Construir e subir os contêineres

```bash
docker compose pull
docker compose up -d
```

!!! alert "Atenção"
    Os contêineres podem demorar alguns minutos para iniciar. e caso o container netbox fique em loop sempre iniciando, use este comando para reiniciar este container:

    ```bash
        docker compose restart netbox
    ```
    e para acessar os logs basta usar o comando:

    ```bash
        docker compose logs -f
    ```

### 1.7 Criar usuário administrador

Após a inicialização dos contêineres:

```bash
docker compose exec netbox /opt/netbox/netbox/manage.py createsuperuser
```

Siga as instruções para definir **usuário, e-mail e senha**.


### 1.8 Acessar a interface web

* URL local: <a target="_blank" href="http://localhost:8000">http://localhost:8000</a>
* De outro host: `http://<IP_DO_SERVIDOR>:8000`

> Substitua a porta se tiver alterado no passo 5.


### 1.9 Resumo de boas práticas para produção

* Alterar todas as credenciais padrão nos arquivos `.env`.
* Configurar certificados TLS (HTTPS) com Nginx ou Traefik.
* Ativar backup regular do banco de dados PostgreSQL.
* Monitorar logs e consumo de recursos dos contêineres.


## 2. Acesso

Após concluir a instalação do NetBox no Docker, você pode acessá-lo via navegador da web. Por padrão, o NetBox estará disponível localmente em <a target="_blank" href="http://localhost:8000/">http://localhost:8000/</a>. No entanto, se você deseja acessar o NetBox de forma segura através de um túnel SSH, siga as etapas abaixo:

### 2.1 Acesso via tunel ssh

1. Agora, para acessar o NetBox de forma segura através de um túnel SSH, você precisará de um servidor remoto com acesso SSH, onde o Docker não precisa estar instalado.
2. No servidor remoto, execute o seguinte comando para criar um túnel SSH para o NetBox:
    
    ```
    ssh -N -L 8080:localhost:8080 usuario@endereco_do_servidor
    ```
    
    - Substitua `usuario` pelo nome de usuário do servidor remoto.
    - Substitua `endereco_do_servidor` pelo endereço IP ou nome de domínio do servidor remoto.
3. Após inserir sua senha SSH, o túnel será estabelecido. Agora, o servidor remoto redirecionará as solicitações da porta 8080 para o NetBox na porta 8000.
4. Em seu computador local, abra o navegador da web e acesse:
    
    ```
    <http://localhost:8080/>
    ```
    
    Você será redirecionado para o NetBox que está sendo executado no servidor remoto por meio do túnel SSH. Agora você pode acessar o NetBox com segurança.
    

Lembre-se de que o túnel SSH manterá a conexão ativa enquanto o terminal do servidor remoto estiver aberto. Se você deseja manter o túnel funcionando em segundo plano, adicione a opção `-f` ao comando SSH no passo 9:

```
ssh -f -N -L 8080:localhost:8000 usuario@endereco_do_servidor
```

Com isso, você poderá acessar o NetBox de forma segura por meio de um túnel SSH, garantindo a proteção dos seus dados durante a transmissão.

## 3. Importação

Para a importação deve-se organizar os arquivos em formato CSV corretamente formatado, contendo os campos indicados a seguir. Além disso, é importante que a importação siga a ordem da numeração dos arquivos conforme consta na preparação dos dados.

### 3.1. Preparação dos dados

A importação dos arquivos csv deve seguir a numeração estabelecida e conter as informações indicadas. Os nomes (**em negrito**) indicam os locais de importação, e as informações abaixo (*em itálico*) indicam os campos necessários para a importação.

1. **manufacturers**
*name, slug*
2. **platforms**
*name, slug, manufacturer, napalm_driver, description*
    
    **tags**
    *name, items, slug, color, description*
    
3. **device_roles**
*name, color, vm_role, description, slug, tag*
    
    **device_types**
    *model, manufacturer, part_number, u_height, is_full_depth, slug*
    
    **sites**
    *name, status, slug, latitude, longitude*
    
    **tenants**
    *name, slug*
    
4. **devices**
*name, status, device_role, manufacturer, device_type, site, platform, tag*
5. **interfaces**
*name, device, label, enabled, type, description*
    
    **VRFs**
    *name, rd, tenant, enforce_unique, description, import_targets, export_targets, comments, tags*
    
6. **circuit_types**
*name, slug*
    
    **IP_addresses**
    *address, vrf, tenant, status, role, device, interface, dns_name, description*
    
    **providers**
    *name, slug*
    
7. **circuits**
*cid, provider, type, status, tenant, description*

### 3.2. A importação

1. **Faça login como superusuário**: Acesse o NetBox com as credenciais de admin.
2. **Encontre a opção de importação**: Verifique a seção relacionada aos dados que deseja importar, e procure por um **ícone** de importação como vemos na Figura 1 abaixo:
    
    ![**Figura 1**: ao clicar no ícone importação é possivel fazer o upload do arquivo CSV.](../../../img/netbox_imgs/import.png)
    **Figura 1**: ao clicar no ícone importação é possivel fazer o upload do arquivo CSV.
    
3. **Selecione o arquivo CSV**: Faça o upload do arquivo CSV com os dados preparados, cada CSV precisa conter os campos conforme descrito a Subseção 3.1.
4. **Inicie a importação**: Clique em "Enviar" ou "Importar" para começar o processo.
5. **Verifique os resultados**: Analise o relatório de importação para confirmar o sucesso.

<aside>
💡 **Observação:** após realizar a importação do arquivos do item `7.`, é necessário incluir as terminações manualmente.
Para isso, sigas as instruções abaixo para completar a configuração. clique no circuito criado e no ícone `edit` conforme destacado na imagem abaixo
Então edite as informações de `side*` e `interface*`
</aside>

- Clique em Circuits para ver os circuitos criados na etapa 7. Selecione com 1 clique um dos Circuit ID criado, conforme o indicado na Figura 2.
    
    **Observação**: as etapas devem ser feitas para todo Circuito ID existente.
    

![**Figura 2**: clique no circuit (seta a esquerda), em seguida selecione o Circuirt ID (detacados e indicados com a seta) para realizar a configuração.](../../../img/netbox_imgs/circuitID.png)
**Figura 2**: clique no circuit (seta a esquerda), em seguida selecione o Circuirt ID (detacados e indicados com a seta) para realizar a configuração.

- Após clicar em um dos circuitos, as configurações do circuito é similar a apresentada na Figura 3. As teminações devem ser editadas clicando no ícone `Edit` conforme destacado na imagem abaixo. Ao clicar no ícone, o Netbox encaminha para a parte de Cables em Conexões, conforme mostra a Figura 4.

![Figura 3: tela de um Circuit ID. As edições de de cada Temination deve ser realizada clicando em `Edit` (destacado com a seta).](../../../img/netbox_imgs/circuitEdit.png)
**Figura 3:** tela de um Circuit ID. As edições de de cada Temination deve ser realizada clicando em `Edit` (destacado com a seta).

- A Figura 4 apresenta a criação dos cabos de conexão, a numeração dos cabos seguem apenas a ordem de criação. Os itens `Side*` e `Interface*` devem ser preenchidos para finalizar a configuração da etapa 7.

![Figura 4: tela de configuração dos cabos para conexão para a conexão entre os dispositivos.](../../../img/netbox_imgs/circuitCable.png)
**Figura 4:** tela de configuração dos cabos para conexão para a conexão entre os dispositivos.

<aside>
💡 Lembre-se de adaptar as subcategorias e locais de importação de acordo com as funcionalidades específicas do seu NetBox. Cada categoria pode ter campos e configurações únicas para a importação.
</aside>
