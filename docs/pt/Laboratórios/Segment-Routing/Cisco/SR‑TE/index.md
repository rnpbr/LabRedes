# SR-TE - Traffic Engineering com Segment Routing

!!! info "Repositório"
    Este conteúdo vem do repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**. Arquivos deste laboratório: <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/labs/cisco/sr-mpls/sr-te">`labs/cisco/sr-mpls/sr-te`</a>.

!!! info "Pré-requisitos"
    [Fundamentos de SR-MPLS](../../index.md#fundamentos-de-sr-mpls).

## :material-bookmark: **O que é SR-TE**

SR-TE é o mecanismo de engenharia de tráfego do Segment Routing: o headend impõe uma lista explícita de segmentos (SIDs) que descreve o caminho desejado, ignorando o que o IGP escolheria pelo custo da métrica. Não há sinalização RSVP-TE nem estado por caminho nos nós intermediários: cada nó apenas encaminha olhando o topo da pilha de labels, exatamente como no encaminhamento SR nativo.

Isso resolve uma limitação estrutural do IGP: o SPF escolhe um único critério (custo), e todo o tráfego para um destino segue o mesmo caminho (ou faz ECMP entre caminhos de custo igual). Quando existe uma razão para separar o tráfego por caminhos diferentes (latência, afinidade, isolamento de risco), o IGP sozinho não tem como expressar isso. O SR-TE resolve no plano de controle do headend, sem alterar o IGP nem os nós de trânsito.

## :material-lightbulb-on-outline: **Conceitos-chave**

| Termo | Significado |
|---|---|
| **Headend** | Nó que origina a SR Policy e impõe a pilha de labels. É o único ponto que conhece a policy. |
| **Endpoint** | Endereço IP de destino da policy, tipicamente a loopback de um PE remoto. |
| **Color** | Atributo numérico da policy. Junto com o endpoint, identifica a policy de forma única. Usado para associar uma intenção (por exemplo, "baixa latência") à policy certa. |
| **Candidate path** | Um caminho possível para a policy, com uma preferência. A policy usa o de maior preferência que estiver válido. |
| **Segment list** | Sequência ordenada de SIDs que descreve um caminho explícito. No plano de dados, vira a pilha de labels MPLS. |
| **Binding-SID** | Label local que representa a policy inteira. Permite que outro nó (ou uma rota estática) empilhe só esse label sem conhecer os segmentos internos. |
| **Waypoint** | Nó intermediário incluído deliberadamente na segment list para forçar a passagem por ele. |

## :material-call-split: **Caminho explícito e caminho dinâmico**

Uma SR Policy pode ter dois tipos de candidate path:

- **Explícito (explicit):** a segment list é definida à mão pelo operador, como uma lista fixa de labels. É o que o lab [`explicit-policy`](explicit-policy.md) usa. É simples de entender e depurar, mas não se adapta a mudanças de topologia: se um nó do caminho cair, a policy fica `down` até alguém reconfigurá-la.
- **Dinâmico (dynamic):** o headend (ou um controlador externo, tipicamente um SR-PCE alimentado por BGP-LS) calcula o caminho com base em um objetivo (menor métrica IGP, menor latência, afinidades a incluir ou excluir) e o recalcula automaticamente se a topologia mudar. Fora do escopo destes laboratórios por enquanto; veja o [roadmap](../../index.md#roadmap).

Em produção, a maioria das implantações usa caminhos dinâmicos ou uma combinação dos dois (explícito como alternativa, dinâmico como preferencial). O caminho explícito é o ponto de entrada didático porque o resultado é previsível e fácil de conferir na pilha de labels.

## :material-sign-direction: **Como o tráfego entra na policy (steering)**

Uma SR Policy existir não basta: é preciso algo que decida qual tráfego vai usá-la. Há três formas:

- **Rota estática com `sr-policy`:** o método usado no lab [`explicit-policy`](explicit-policy.md). Simples, mas manual: cada prefixo que deve usar a policy precisa de uma rota estática dedicada.
- **Automated Steering (Color):** o BGP anuncia o prefixo com uma community de Color. O headend associa o Color do prefixo ao Color de uma SR Policy existente e direciona o tráfego automaticamente, sem rota estática por prefixo. É o mecanismo usado em produção para ganhar escala.
- **ODN (On-Demand Nexthop):** o headend nem tem a policy pré-configurada; a criação é disparada dinamicamente quando chega o primeiro prefixo com aquele Color, a partir de um template de política. Reduz a configuração manual em redes com muitas policies. Planejado; veja o [roadmap](../../index.md#roadmap).

## :material-link-variant: **Binding-SID e stitching**

O Binding-SID é o que permite compor policies: um headend em um domínio pode empilhar o Binding-SID de uma policy que existe só no domínio seguinte, sem precisar conhecer os segmentos internos daquele domínio. Essa é a base de cenários interdomínio (costura de policies através de fronteiras administrativas), ainda não coberta por um laboratório; veja o [roadmap](../../index.md#roadmap).

## :material-compare: **SR-TE vs Flexible Algorithm**

Os dois resolvem problemas parecidos (um caminho diferente do SPF padrão) por mecanismos diferentes:

- **SR-TE** opera por policy, no headend, por color e endpoint. A granularidade é de fluxo ou serviço: policies diferentes podem levar tráfegos diferentes para o mesmo destino por caminhos diferentes.
- **Flex-Algo** opera no IGP inteiro: todo nó do domínio calcula um SPF alternativo com as mesmas restrições (afinidades, métrica alternativa), e o resultado é um Prefix-SID por algoritmo, válido para qualquer origem. A granularidade é de topologia, não de fluxo.

Na prática, os dois se combinam: o Flex-Algo constrói o plano de encaminhamento restrito, e o SR-TE pode usar SIDs desse algoritmo dentro de uma segment list. O lab [`flex-algo-anycast`](../Multidomínio/flex-algo-anycast.md) faz exatamente isso: uma segment list explícita feita de SIDs do algoritmo 128. Veja os [conceitos de multidomínio](../Multidomínio/index.md).

## :material-file-document-multiple: **Laboratórios desta trilha**

| Lab | O que mostra | Nós |
|---|---|---:|
| [explicit-policy](explicit-policy.md) | Segment list estática forçando um caminho de menor latência | 5 |
