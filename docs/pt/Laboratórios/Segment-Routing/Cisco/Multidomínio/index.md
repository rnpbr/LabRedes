# Multidomínio - Flex-Algo e SID anycast entre domínios IGP

!!! info "Repositório"
    Este conteúdo vem do repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**. Arquivos deste laboratório: <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/labs/cisco/sr-mpls/multidominio">`labs/cisco/sr-mpls/multidominio`</a>.

!!! info "Pré-requisitos"
    [fundamentos de SR-MPLS](../../index.md).

## :material-bookmark: **O problema**

Operadores dividem o IGP em vários domínios por escala, contenção de falhas e
fronteiras operacionais. O preço é que nenhum roteador enxerga a topologia
completa. Um Prefix-SID só existe no domínio que o inunda: o PE de entrada não
tem LSA, rota nem label para o PE do outro lado, e não consegue calcular um SPF
até ele.

A solução de transporte precisa, portanto, de algum elemento que conheça o
caminho entre domínios e o traduza em segmentos que cada domínio saiba executar.

## Formas de costurar os domínios

| Mecanismo | Quem conhece o caminho interdomínio | Onde está neste projeto |
|---|---|---|
| BGP-LU / seamless MPLS | o BGP, prefixo a prefixo, com label e next hop | [Inter-AS](../Inter‑AS/index.md) e lab `bgp-lu` |
| SR-PCE alimentado por BGP-LS | um controlador com a topologia de todos os domínios | planejado |
| ODN / Automated Steering | o headend, disparado pelo color da rota de serviço, normalmente com PCE | planejado |
| Lista explícita com SIDs de borda | o operador, que monta a pilha à mão | lab `flex-algo-anycast` |

A última forma é um degrau didático: deixa o plano de controle fácil de
inspecionar porque o humano faz o papel do elemento de computação interdomínio.
Não é a resposta de produção, e o lab que a usa trata essa limitação como parte
do conteúdo.

## Multiprocesso não é multiárea

Os domínios do lab são **processos OSPF independentes**, cada um em área `0`, e
os roteadores de borda rodam um processo por domínio sem redistribuição entre
eles. Nada atravessa a fronteira: nem prefixos, nem SIDs, nem a topologia.

Em OSPF multiárea a situação é outra. O ABR resume prefixos entre áreas, e o
Prefix-SID pode ser propagado com o prefixo (RFC 8665). Algo semelhante vale
para IS-IS multinível com vazamento de rotas entre níveis. Nesses desenhos o alcance interdomínio existe no
IGP e o problema descrito acima não aparece da mesma forma.

## Flexible Algorithm

Flex-Algo (RFC 9350) acrescenta ao IGP algoritmos de SPF identificados por um
número entre 128 e 255. Cada algoritmo é descrito por uma **Flexible Algorithm
Definition** (FAD):

- **tipo de métrica:** IGP, atraso ou métrica TE;
- **tipo de cálculo:** SPF;
- **restrições:** afinidades a excluir ou exigir (`exclude-any`, `include-any`,
  `include-all`), entre outras.

A FAD é inundada pelo IGP. Se mais de um nó anunciar definições diferentes para
o mesmo número, vence a de maior prioridade e, no empate, a do maior router-id.
Cada nó anuncia também em quais algoritmos participa; só os participantes entram
na topologia daquele algoritmo.

Um prefixo pode ter um Prefix-SID por algoritmo. O resultado é um plano de
encaminhamento paralelo: o label do algoritmo 128 para um destino segue o
caminho calculado com as restrições do algoritmo 128, valendo para qualquer
origem do domínio. Isso o distingue de uma SR Policy, que é estado só do
headend; ver [SR-TE vs Flexible Algorithm](../SR‑TE/index.md#sr-te-vs-flexible-algorithm).

### Afinidades

Uma afinidade (*admin group*) é um bit associado ao enlace. Em OSPF, a afinidade
usada pelo Flex-Algo é anunciada nos atributos de enlace específicos de
aplicação (ASLA, RFC 9492), e não no atributo TE genérico. Um enlace marcado com
a cor excluída pela FAD simplesmente não existe na topologia daquele algoritmo.

Para mostrar a diferença, basta deixar o enlace marcado mais barato que o
caminho limpo: o SPF default o escolhe, o algoritmo 128 não.

### Flex-Algo é por domínio

A FAD vale dentro do domínio que a inunda. Nada no protocolo garante que o
algoritmo 128 de um domínio signifique o mesmo que o algoritmo 128 do vizinho.
Quando uma pilha usa SIDs do algoritmo 128 em domínios diferentes, a coerência
de intenção - "evite os enlaces red" - é uma convenção operacional: a mesma FAD
precisa ser configurada em todos eles.

## SID anycast

Um SID anycast é um Prefix-SID anunciado por mais de um nó para o **mesmo**
prefixo, com o **mesmo** índice (RFC 8402, seção 3.3). Cada roteador encaminha
o label ao anunciante mais próximo, segundo o algoritmo do SID. Para que o
label seja o mesmo em todos os membros, o índice e a SRGB precisam coincidir.

Na borda entre domínios ele dá redundância sem fixar um roteador: a pilha diz
"entregue a qualquer borda AB" em vez de "entregue ao DBR-AB1". Se uma borda
deixa de ser alcançável, o IGP local passa a escolher a outra, sem mudar a
pilha.

O anúncio deve sinalizar que o prefixo não identifica um único nó. Em OSPFv2
isso é a N-flag do Extended Prefix TLV (RFC 7684), que deve ficar desligada para
anycast; uma loopback comum a anuncia ligada. Os flags do SID sub-TLV não
carregam essa informação.

### O risco do SID anycast de borda

O SID anycast prova que uma borda é **alcançável a partir do domínio local**.
Ele não prova que essa borda ainda consegue encaminhar para o **próximo**
domínio.

Se um roteador de borda perde todos os enlaces do lado seguinte, mas mantém a
adjacência do lado de cá, continua anunciando o anycast no domínio de origem e
continua atraindo o tráfego. Ao chegar nele, o próximo segmento não tem entrada
na LFIB e o pacote é descartado. O domínio de origem não tem como perceber: a
falha ocorreu num IGP que ele não enxerga.

O headend também pode não perceber. No IOS-XR usado no lab, uma lista explícita
de labels é validada pelo primeiro segmento, que continua resolvido; a policy
permanece operacional enquanto o tráfego cai.

Desenhos de produção precisam de um mecanismo que retire o anúncio anycast, ou
reduza sua preferência, quando a conectividade com o domínio seguinte falha -
anúncio condicionado à saúde do lado seguinte, por exemplo - ou de um elemento
de computação com visão dos dois lados, como um PCE alimentado por BGP-LS.

## :material-alert: **Antes de transportar o desenho**

Isto é material de laboratório, não um baseline de produção:

- não use listas explícitas montadas à mão como transporte interdomínio;
- trate anycast de borda junto com um mecanismo de retirada condicionada;
- padronize a FAD de cada algoritmo em todos os domínios que compartilham uma
  pilha, e documente essa convenção;
- detecte falhas com BFD; sem ele, a detecção depende do dead interval do OSPF;
- verifique MSD e comportamento de PHP na plataforma alvo antes de assumir a
  profundidade de pilha usada no lab.

## :material-book-alphabet: **Glossário**

**Afinidade.** Bit administrativo associado a um enlace (*admin group*), usado
como restrição por Flex-Algo e SR-TE.

**DBR.** *Domain Border Router* neste projeto: roteador que pertence a dois
domínios IGP e roda um processo por domínio.

**FAD.** *Flexible Algorithm Definition*: métrica, tipo de cálculo e restrições
de um algoritmo Flex-Algo.

**N-flag.** Flag do Extended Prefix TLV do OSPFv2 que indica que o prefixo
identifica um nó. Desligada em prefixos anycast.

**SID anycast.** Prefix-SID anunciado por vários nós para o mesmo prefixo, com o
mesmo índice.

Termos gerais de SR - Prefix-SID, Node-SID, SRGB, segment list e SR Policy -
estão nos [fundamentos de SR-MPLS](../../index.md).

## :material-file-document-multiple: **Laboratórios desta trilha**

| Página | Para que serve |
|---|---|
| [flex-algo-anycast](flex-algo-anycast.md) | Três domínios OSPF sem redistribuição, Flex-Algo 128 e SIDs anycast de borda (10 roteadores) |
| [validacao](validacao.md) | O que as execuções de referência confirmaram, e o que não |

## :material-book-open-variant: **Referências**

- RFC 9350 - *IGP Flexible Algorithm*: <https://www.rfc-editor.org/rfc/rfc9350.html>
- RFC 8402 - *Segment Routing Architecture*, seção 3.3 (IGP-Anycast Segment): <https://www.rfc-editor.org/rfc/rfc8402.html>
- RFC 8665 - *OSPF Extensions for Segment Routing*: <https://www.rfc-editor.org/rfc/rfc8665.html>
- RFC 7684 - *OSPFv2 Prefix/Link Attribute Advertisement*: <https://www.rfc-editor.org/rfc/rfc7684.html>
- RFC 9492 - *OSPF Application-Specific Link Attributes*: <https://www.rfc-editor.org/rfc/rfc9492.html>
- RFC 7308 - *Extended Administrative Groups in MPLS Traffic Engineering*: <https://www.rfc-editor.org/rfc/rfc7308.html>
- RFC 9256 - *Segment Routing Policy Architecture*: <https://www.rfc-editor.org/rfc/rfc9256.html>
- RFC 9552 - *Distribution of Link-State and Traffic Engineering Information Using BGP*: <https://www.rfc-editor.org/rfc/rfc9552.html>
