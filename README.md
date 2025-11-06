# Grafo de Bairros do Recife

Implementação de um grafo não direcionado com arestas paralelas para representar bairros do Recife e suas conexões através de vias.

## Descrição

Este projeto implementa um grafo que representa:
- **Vértices**: Bairros do Recife, organizados por subregião
- **Arestas**: Vias que conectam os bairros
- **Pesos**: Distância em metros de cada via

O grafo suporta arestas paralelas, permitindo que dois bairros sejam conectados por múltiplas vias diferentes.

## Estrutura do Projeto

```
.
├── grafo.py           # Classes principais: Grafo, Vertice, Aresta
├── carregar_dados.py  # Funções para carregar dados das planilhas
├── main.py            # Script principal
└── README.md          # Este arquivo
```

## Classes Principais

### Vertice
Representa um bairro do grafo.
- `nome`: Nome do bairro
- `subregiao`: Subregião a que pertence

### Aresta
Representa uma via que conecta dois bairros.
- `origem`: Bairro de origem
- `destino`: Bairro de destino
- `nome_via`: Nome da via (logradouro)
- `peso`: Distância em metros

### Grafo
Implementação do grafo não direcionado.
- `adicionar_vertice()`: Adiciona um bairro
- `adicionar_aresta()`: Adiciona uma via entre dois bairros
- `obter_vizinhos()`: Retorna todas as conexões de um bairro
- `obter_arestas_entre()`: Retorna todas as vias entre dois bairros
- `grau()`: Retorna o número de conexões de um bairro
- `estatisticas()`: Exibe estatísticas do grafo

## Requisitos

- Python 3.6+
- pandas
- openpyxl (para ler arquivos Excel)

Instalação:
```bash
pip install pandas openpyxl
```

## Uso

### Uso básico:

```bash
python main.py
```

### Especificar caminhos customizados:

```bash
python main.py --subregioes /caminho/para/bairros_por_subregiao.xlsx --vias /caminho/para/vias.xlsx
```

### Uso programático:

```python
from carregar_dados import construir_grafo_completo

# Construir o grafo
grafo = construir_grafo_completo(
    caminho_subregioes='bairros_por_subregiao_limpo.xlsx',
    caminho_vias='Todas as vias FINAL (1).xlsx'
)

# Obter informações de um bairro
vertice = grafo.obter_vertice("Boa Viagem")
print(f"Bairro: {vertice.nome}, Subregião: {vertice.subregiao}")

# Listar vizinhos
vizinhos = grafo.obter_vizinhos("Boa Viagem")
for aresta in vizinhos:
    print(f"{aresta.destino} via {aresta.nome_via} ({aresta.peso}m)")

# Verificar arestas paralelas
arestas = grafo.obter_arestas_entre("Água Fria", "Beberibe")
print(f"Existem {len(arestas)} vias conectando esses bairros")
```

## Formato das Planilhas

### bairros_por_subregiao_limpo.xlsx
- Cada coluna representa uma subregião (ex: 1.1, 1.2, 1.3, etc.)
- Cada célula contém o nome de um bairro
- Células vazias (NaN) são ignoradas

### Todas as vias FINAL (1).xlsx
Deve conter as seguintes colunas:
- `bairro_origem`: Bairro de origem
- `bairro_destino`: Bairro de destino
- `nome_logradouro`: Nome da via
- `distancia_metros`: Distância em metros

## Características

- Grafo não direcionado: se A conecta a B, então B conecta a A
- Suporte a arestas paralelas: dois bairros podem ter múltiplas vias conectando-os
- Estrutura simples e didática, adequada para fins acadêmicos
- Sem dependências de bibliotecas de grafos (networkx, igraph, etc.)

## Exemplo de Saída

```
==============================================================
CONSTRUINDO GRAFO DE BAIRROS
==============================================================

Passo 1: Carregando vértices (bairros)...
Carregando vértices de: /mnt/c/Users/luise/Downloads/bairros_por_subregiao_limpo.xlsx
✓ 94 vértices adicionados

Passo 2: Carregando arestas (vias)...
Carregando arestas de: /mnt/c/Users/luise/Downloads/Todas as vias FINAL (1).xlsx
✓ 904 arestas adicionadas

==============================================================
GRAFO CONSTRUÍDO COM SUCESSO!
==============================================================

==============================================================
ESTATÍSTICAS DO GRAFO
==============================================================
Número de vértices (bairros): 94
Número de arestas (vias): 904
Grau médio: 19.23
Bairro com mais conexões: Recife (grau: 42)
Número de subregiões: 18
==============================================================
```

## Notas Técnicas

- O grafo utiliza um dicionário para armazenar vértices (acesso O(1))
- Lista de adjacências para armazenar conexões
- Cada aresta é armazenada duas vezes (ida e volta) para facilitar consultas
- Normalização de nomes (strip) para evitar problemas com espaços

## Autor

Projeto desenvolvido para a disciplina de Estrutura de Dados e Algoritmos.
