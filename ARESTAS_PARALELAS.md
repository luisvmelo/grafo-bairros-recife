# Entendendo as Arestas Paralelas

## O que são arestas paralelas?

Arestas paralelas são **múltiplas arestas conectando o mesmo par de vértices**. No nosso grafo de bairros, isso significa que dois bairros podem ser conectados por várias vias diferentes.

## Exemplo Prático: Água Fria

### Estatísticas
- **51 vias totais** (arestas)
- **7 bairros conectados** (conexões únicas)
- **Média de ~7 vias por bairro vizinho**

### Detalhamento

| Bairro Destino | Número de Vias | Exemplos de Vias |
|----------------|----------------|------------------|
| Fundão | 13 vias | Av. Anibal Benevolo, Rua Alto Bonito, Rua Violeta, etc. |
| Arruda | 11 vias | Av. Beberibe, Rua Bom Conselho, Rua Das Mocas, etc. |
| Campina do Barreto | 5 vias | Rua Constanca, Rua Coronel Urbano Ribeiro, etc. |
| Linha do Tiro | 9 vias | - |
| Porto da Madeira | 7 vias | - |
| Beberibe | 2 vias | Av. Anibal Benevolo, Av. Beberibe |
| Torreão | 4 vias | - |

**Total: 51 vias conectando 7 bairros**

## Por que isso acontece?

Dois bairros podem ter múltiplas vias de conexão por diversos motivos:
1. **Bairros grandes**: Bairros com grande extensão territorial têm múltiplas ruas fazendo fronteira
2. **Vias paralelas**: Várias ruas que correm paralelas conectando os mesmos bairros
3. **Malha viária densa**: Áreas urbanas com muitas opções de trajeto

## Impacto na Visualização

### Antes da correção:
- Mostrava apenas **uma linha** entre Água Fria e Fundão
- Difícil de perceber que existem 13 vias diferentes

### Depois da correção:
- **Linha mais grossa** indica mais vias paralelas
- **Número na linha** mostra quantas vias existem (ex: "13")
- **Tooltip** (passar o mouse) lista todas as vias
- **Estatísticas** separadas:
  - 🛣️ Vias Totais: 904 (todas as vias)
  - 🔗 Conexões Únicas: 257 (pares únicos de bairros)

## Estatísticas Gerais do Grafo

```
Total de vias (arestas): 904
Pares únicos de bairros conectados: ~257
Média de vias por conexão: ~3.5 vias

Top 5 conexões com mais vias paralelas:
1. Água Fria ↔ Fundão: 13 vias
2. Água Fria ↔ Arruda: 11 vias
3. ... (continue explorando no grafo)
```

## Como verificar no código

```python
from carregar_dados import construir_grafo_completo

grafo = construir_grafo_completo(caminho_subregioes, caminho_vias)

# Ver todas as vias entre dois bairros
arestas = grafo.obter_arestas_entre("Água Fria", "Fundão")
print(f"Número de vias: {len(arestas)}")

for aresta in arestas:
    print(f"- {aresta.nome_via} ({aresta.peso:.2f}m)")
```

## Conclusão

As **arestas paralelas são uma característica importante** deste grafo, refletindo a realidade urbana onde múltiplas vias conectam os mesmos bairros. A visualização foi ajustada para representar essa característica de forma clara e intuitiva.
