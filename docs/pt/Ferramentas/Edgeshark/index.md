# Guia de Instalação e Uso do Edgeshark

## 1. Introdução

**Edgeshark** é uma solução inovadora projetada para facilitar a captura e análise de tráfego de rede em ambientes containerizados. Ele consiste em dois serviços containerizados principais, o <a target="_blank" href="https://github.com/siemens/ghostwire">Ghostwire</a> e o <a target="_blank" href="https://github.com/siemens/packetflix">Packetflix</a>, que trabalham em conjunto para monitorar o tráfego de rede dentro de contêineres Docker. Além disso, oferece um plugin opcional para o Wireshark, chamado <a target="_blank" href="https://github.com/siemens/cshargextcap">csharg external capture plugin</a>, que permite capturas remotas ao vivo do tráfego de rede.

## 2. instalando o Edgeshark

O Edgeshark oferece imagens Docker multi-arquitetura para as arquiteturas `linux/amd64` e `linux/arm64`.

!!! warning "ATENÇÃO"
    Certifique-se de que você tem um kernel Linux de pelo menos a versão 4.11 instalado. No entanto, recomendamos fortemente usar a versão 5.6 ou superior.

=== "Usando Docker Compose v2"

    1. **Instale o Docker Compose v2:**

    Certifique-se de que o plugin Docker Compose v2 esteja instalado. Verifique executando `docker compose version`, que deve exibir a versão do plugin sem erros. Para usuários Debian, recomendamos instalar os pacotes `docker-ce` em vez de `docker.io`, pois são atualizados com mais frequência.

    2. **Implantação dos serviços Edgeshark:**
    
       Copie e cole o comando abaixo em um terminal para implantar os serviços:
    
         
        wget -q --no-cache -O - \
        https://github.com/siemens/edgeshark/raw/main/deployments/wget/docker-compose-localhost.yaml \
        | DOCKER_DEFAULT_PLATFORM= docker compose -f - up
        
    
       3. **Acesse a interface:**
    
          Após a implantação, visite <a target="_blank" href="http://localhost:5001/">http://localhost:5001</a> no seu navegador para explorar a rede virtual do seu host de contêiner.
    
    
    !!! note "NOTA"
        Usar DOCKER_DEFAULT_PLATFORM= garante a implantação correta das imagens multi-arquitetura e evita problemas, especialmente com o Rosetta da Apple, que pode ter dificuldades com implantações de imagens em modo somente leitura.
    
    
    !!! warning "AVISO"
        As implantações rápidas a seguir exporão a porta TCP 5001 (ou 5500) para clientes externos ao seu host. Certifique-se de que sua rede está devidamente protegida.
    

=== "Usando Bash"

    Se o seu sistema não suportar Docker Compose v2, você pode usar um script Bash como alternativa.

    1. **Implantação via Bash:**
    
       Execute o comando abaixo para implantar os serviços usando um script Bash:

        wget -q --no-cache -O - \\
          <https://github.com/siemens/edgeshark/raw/main/deployments/nocomposer/edgeshark.sh> \\
          | DOCKER_DEFAULT_PLATFORM= bash -s up
    
    2. **Acesse a interface:**

        Visite <a target="_blank" href="http://localhost:5001/">http://localhost:5001</a> no seu navegador para explorar a rede virtual do seu host de contêiner.
    
    
    !!! warning "AVISO"
        As implantações Esta implantação rápida exporá a porta TCP 5001 para clientes externos ao seu host. Certifique-se de que sua rede está devidamente protegida.
    

=== "Usando Industrial Edge"

    1. **Baixe o aplicativo Edgeshark:**
    
        Baixe o <a href="https://github.com/siemens/edgeshark/releases/latest" target="_blank">último arquivo `.zip`</a> na seção de lançamentos do projeto.

    2. **Extraia o arquivo:**   

        Descompacte o arquivo `edgeshark.app` contido no arquivo `.zip`.

    3. **Importe para o IEM:**

         Importe o arquivo `edgeshark.app` no seu sistema de gerenciamento Industrial Edge (IEM).

    4. **Implantação no IED:**

         No catálogo do seu IEM, implante o aplicativo Edgeshark nos seus dispositivos Industrial Edge (IED).

        !!! warning "AVISO" 
            A interface do Edgeshark e os serviços são expostos na porta 5001 nos seus hosts IED sem qualquer autorização de usuário. Isso é necessário para suportar a captura remota de pacotes a partir da interface de usuário.
    

    5. **Acesse a interface:**

        Navegue até a porta HTTP 5001 no seu IED: `http://<endereço-ip-do-ied>:5001` (certifique-se de usar `http:` e **não** `https:`). Agora você deve ver a interface de usuário do Edgeshark.

### 2.1 Plugin Opcional para Captura de Pacotes

Caso você precise capturar tráfego de rede ao vivo dentro dos contêineres, é necessário instalar o plugin externo <a target="_blank" href="https://github.com/siemens/cshargextcap">cshargextcap</a> para o Wireshark.

=== "Windows 64bit"

    1. **Verifique o Wireshark:**  
       Certifique-se de que você tem uma versão recente do <a target="_blank" href="https://wireshark.org">Wireshark (64 bits)</a> instalada. A versão mínima recomendada é a 3.0.2.
    
    2. **Instale o plugin:**  
        Baixe e execute o instalador mais recente do plugin, disponível <a target="_blank" href="https://github.com/siemens/cshargextcap/releases/latest">aqui</a>.
    
    3. **Inicie a captura:**  
        Na interface web do Edgeshark, clique em um dos botões de Wireshark para iniciar uma sessão de captura.

=== "Linux 64bit"

    1. **Instale o Wireshark:**  
       Instale o Wireshark a partir dos repositórios da sua distribuição e permita que ele seja usado por usuários não root.
    
    2. **Adicione seu usuário ao grupo wireshark:**  
        Execute o comando abaixo:

            sudo gpasswd -a $USER wireshark

    3. **Instale o plugin:**  
       Baixe e instale o pacote do plugin apropriado para sua distribuição.
    
    4. **Inicie a captura:**  
        Na interface web do Edgeshark, clique em um dos botões de Wireshark para iniciar uma sessão de captura.

=== "macOS 64bit"

    1. **Baixe o plugin:**  
        Baixe o plugin mais recente para macOS <a href="https://github.com/siemens/cshargextcap/releases/latest" target="_blank">aqui</a>

    2. **Instale o plugin:**  
         Siga as instruções de instalação fornecidas no arquivo baixado.

    3. **Inicie a captura:**  
        Navegue até a interface web do Edgeshark e clique em um botão de Wireshark para iniciar uma captura ao vivo.


## Próximos Passos

Agora que o Edshark está instalado, o próximo passo é aprender a utilizá-lo de maneira eficaz. Para isso, acesse a página de uso detalhado clicando [aqui](#) e descubra como capturar o tráfego de rede em seus contêineres utilizando o Edgeshark. Aproveite os recursos disponíveis para otimizar a coleta de dados e melhorar a visibilidade da sua rede.

## Referências

Para mais informações e recursos adicionais sobre o Edgeshark, visite a <a href="https://edgeshark.siemens.io/#/getting-started" target="_blank">Documentação Oficial</a>.

