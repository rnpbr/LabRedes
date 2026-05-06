# Guia : Criando Imagens para Representar Laboratórios

Este guia ensina como criar imagens representando topologias de rede para os laboratórios, utilizando o template do <a target="_blank" href="http://draw.io/">Draw.io</a> fornecido no repositório. As imagens devem seguir a identidade visual do projeto e ser salvas no formato **SVG** dentro da pasta correta.

---

### 1. **Abrindo o Template**

Na raiz do repositório `docs/Templates`, você encontrará um template do <a target="_blank" href="http://draw.io/">**Draw.io**</a>. que pode vê-lo abaixo Abra o arquivo e verá que ele já contém todos os componentes necessários para criar topologias de rede, incluindo:

![Template do Draw.io](../../../img/Template_redes_abertas.svg)

- **Cards de Aplicações**: Representam ativos ou protocolos como **Grafana** e **OpenConfig**.
- **Componentes de Rede**: Ícones de **roteadores**, **switches** e **servidores**.

---

### 2. **Montando a Topologia**

1. **Adicione Componentes de Rede**: Copie e cole os ícones de **roteadores**, **switches** e **servidores** da área de componentes do template.
2. **Adicione Cards de Aplicações**: Posicione os cards que representam os ativos/protocolos na topologia.
3. **Conecte os Componentes**: Use **linhas** (para interconexões) e **setas** (para direcionar para os IPs) para conectar os componentes e criar a estrutura de rede.

### Especificações de Estilo para a Topologia

| Elemento | Especificação |
| --- | --- |
| **Fonte de Título** | **Fonte**: Times New Roman, **Tamanho**: 28px |
| **Fonte de Subtítulo** | **Fonte**: Times New Roman, **Tamanho**: 25px |
| **Linhas de Conexão** | **Espessura**: 11px, **Tipo**: Linhas retas (para interconexões) |
| **Setas para IPs** | **Espessura**: 11px, **Tipo**: Setas (para direcionar para os IPs) |
| **Caixas de Interface** | **Tamanho da Fonte**: 11px |

Com essas especificações, você garante que as topologias sigam o padrão visual do projeto e fiquem consistentes com o restante da documentação.

---

### 3. **Adicionando Interfaces e IPs**

1. **Crie a Caixa de Texto para Interfaces**: Para cada conexão, desenhe um quadrado representando a interface.
2. **Adicione Propriedade de IP**:
    - Selecione o quadrado.
    - Clique com o botão direito e escolha **Adicionar/Editar dados**.
    - Clique em **Adicionar Propriedade**, coloque o nome como **ip** e adicione o endereço IP da interface.

Quando o mouse passar sobre o quadrado, o IP será exibido como uma dica de ferramenta.

---

### 4. **Salvando a Imagem**

Após finalizar a topologia, salve a imagem no formato **SVG**:

1. **Salve como SVG**: No <a target="_blank" href="http://draw.io/">**Draw.io**</a>, vá em **Arquivo > Exportar Como > svg**.
2. **Pasta de Destino**: Salve a imagem na pasta `docs/img/labs_imgs/`.

!!! warning "Atenção"
    Certifique-se de selecionar na hora de exportar selecionar na opção **Appearance:** como Light.

---

### 5. **Atualizando a Documentação**

Após salvar a imagem, atualize o arquivo Markdown da documentação, incluindo a imagem da topologia:

```markdown
![Diagrama de Topologia de Rede](../../labs_imgs/nome-do-lab/nome-da-imagem.svg)

```

---
