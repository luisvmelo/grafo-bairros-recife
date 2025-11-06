"""
Visualização interativa do grafo usando HTML
(Não requer bibliotecas externas além de pandas)
"""
import json
import html
from carregar_dados import construir_grafo_completo


def gerar_html_interativo(grafo, arquivo_saida='grafo_interativo.html'):
    """
    Gera uma visualização HTML interativa do grafo usando vis.js

    Args:
        grafo: Instância do grafo
        arquivo_saida: Nome do arquivo HTML de saída
    """
    print("Gerando visualização interativa HTML...")

    # Preparar dados dos nós
    nos = []
    for nome, vertice in grafo.vertices.items():
        grau = grafo.grau(nome)

        # Tamanho baseado no grau
        tamanho = 10 + grau * 2

        # Cor baseada na subregião
        if vertice.subregiao:
            cores_subregioes = {
                '1.1': '#FF6B6B', '1.2': '#4ECDC4', '1.3': '#45B7D1',
                '2.1': '#FFA07A', '2.2': '#98D8C8', '2.3': '#6C5CE7',
                '3.1': '#FDCB6E', '3.2': '#E17055', '3.3': '#74B9FF',
                '4.1': '#A29BFE', '4.2': '#FD79A8', '4.3': '#FDCB6E',
                '5.1': '#00B894', '5.2': '#00CEC9', '5.3': '#81ECEC',
                '6.1': '#FAB1A0', '6.2': '#FF7675', '6.3': '#FD79A8'
            }
            cor = cores_subregioes.get(vertice.subregiao, '#95A5A6')
        else:
            cor = '#95A5A6'

        nos.append({
            'id': nome,
            'label': nome,
            'title': f"{nome}<br>Subregião: {vertice.subregiao}<br>Conexões: {grau}",
            'value': tamanho,
            'color': cor
        })

    # Preparar dados das arestas - DESENHAR TODAS AS ARESTAS INDIVIDUALMENTE
    arestas = []
    arestas_adicionadas = set()
    total_arestas_reais = 0

    for origem in grafo.adjacencias:
        for aresta in grafo.adjacencias[origem]:
            # Criar um ID único para cada aresta (incluindo o nome da via)
            # para permitir arestas paralelas
            aresta_id = (origem, aresta.destino, aresta.nome_via, aresta.peso)

            # Evitar duplicatas (grafo não direcionado - só desenhar uma vez)
            aresta_reversa_id = (aresta.destino, origem, aresta.nome_via, aresta.peso)

            if aresta_id not in arestas_adicionadas and aresta_reversa_id not in arestas_adicionadas:
                # Todas as arestas com a mesma largura fina
                largura = 1

                # Título mostrando detalhes da via
                titulo = f"<b>{aresta.nome_via}</b><br>Distância: {aresta.peso:.2f}m<br>{origem} ↔ {aresta.destino}"

                arestas.append({
                    'from': origem,
                    'to': aresta.destino,
                    'title': titulo,
                    'width': largura,
                    'length': min(300, aresta.peso / 5)
                })

                arestas_adicionadas.add(aresta_id)
                total_arestas_reais += 1

    # Template HTML
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Grafo de Bairros do Recife</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }}
        #header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        #info {{
            background: #f8f9fa;
            padding: 15px;
            text-align: center;
            border-bottom: 2px solid #dee2e6;
        }}
        #mynetwork {{
            width: 100%;
            height: 85vh;
            border: 1px solid #ddd;
        }}
        .stats {{
            display: inline-block;
            margin: 0 20px;
            font-weight: bold;
        }}
        #controls {{
            position: absolute;
            top: 120px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
        }}
        button {{
            margin: 5px 0;
            padding: 8px 15px;
            width: 100%;
            cursor: pointer;
            border: none;
            background: #667eea;
            color: white;
            border-radius: 5px;
            font-weight: bold;
        }}
        button:hover {{
            background: #764ba2;
        }}
        #legend {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 300px;
        }}
        .legend-title {{
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 14px;
        }}
        .legend-item {{
            margin: 5px 0;
            font-size: 12px;
        }}
        #search-box {{
            position: absolute;
            top: 120px;
            left: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
            width: 250px;
        }}
        #search-input {{
            width: 100%;
            padding: 10px;
            border: 2px solid #667eea;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }}
        #search-results {{
            max-height: 300px;
            overflow-y: auto;
            margin-top: 10px;
        }}
        .search-result-item {{
            padding: 8px;
            cursor: pointer;
            border-bottom: 1px solid #eee;
            transition: background 0.2s;
        }}
        .search-result-item:hover {{
            background: #f0f0f0;
        }}
        .search-result-item:last-child {{
            border-bottom: none;
        }}
        .highlight-node {{
            font-weight: bold;
            color: #667eea;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>🗺️ Grafo de Bairros do Recife</h1>
        <p>Visualização Interativa das Conexões entre Bairros</p>
    </div>

    <div id="info">
        <span class="stats">📍 Vértices (Bairros): {grafo.num_vertices()}</span>
        <span class="stats">🛣️ Arestas (Vias): {total_arestas_reais}</span>
        <span class="stats">📊 Grau Médio: {sum(grafo.grau(v) for v in grafo.vertices) / len(grafo.vertices):.2f}</span>
    </div>

    <div id="controls">
        <h3 style="margin-top: 0;">Controles</h3>
        <button onclick="network.fit()">🔍 Ajustar Zoom</button>
        <button onclick="togglePhysics()">⚡ Toggle Física</button>
        <button onclick="network.stabilize()">🎯 Estabilizar</button>
    </div>

    <div id="search-box">
        <h3 style="margin-top: 0; margin-bottom: 10px;">🔍 Buscar Bairro</h3>
        <input type="text" id="search-input" placeholder="Digite o nome do bairro..." />
        <div id="search-results"></div>
    </div>

    <div id="legend">
        <div class="legend-title">📌 Legenda</div>
        <div class="legend-item">• <b>Tamanho do nó</b> = Número de vias do bairro</div>
        <div class="legend-item">• <b>Cor do nó</b> = Subregião do bairro</div>
        <div class="legend-item">• <b>Cada linha</b> = Uma via individual</div>
        <div class="legend-item">• <b>Múltiplas linhas</b> = Arestas paralelas (múltiplas vias)</div>
        <div class="legend-item">• <b>Passe o mouse</b> para ver nome e distância da via</div>
        <div class="legend-item">• <b>Clique e arraste</b> para mover</div>
        <div class="legend-item">• <b>Scroll</b> para zoom</div>
    </div>

    <div id="mynetwork"></div>

    <script type="text/javascript">
        console.log('Iniciando carregamento do grafo...');

        // Dados
        try {{
            var nodesData = {json.dumps(nos)};
            var edgesData = {json.dumps(arestas)};

            var nodes = new vis.DataSet(nodesData);
            var edges = new vis.DataSet(edgesData);

            console.log('Nós carregados:', nodes.length);
            console.log('Arestas carregadas:', edges.length);
        }} catch(e) {{
            console.error('Erro ao carregar dados:', e);
            alert('Erro ao carregar o grafo. Verifique o console para detalhes.');
            throw e;
        }}

        // Container
        var container = document.getElementById('mynetwork');

        if (!container) {{
            console.error('Container mynetwork não encontrado!');
        }}

        // Data
        var data = {{
            nodes: nodes,
            edges: edges
        }};

        console.log('Data preparada');

        // Options
        var options = {{
            nodes: {{
                shape: 'dot',
                scaling: {{
                    min: 10,
                    max: 50
                }},
                font: {{
                    size: 12,
                    face: 'Arial'
                }},
                borderWidth: 2,
                borderWidthSelected: 4
            }},
            edges: {{
                width: 1,
                color: {{
                    color: '#848484',
                    highlight: '#FF0000',
                    hover: '#FF0000'
                }},
                smooth: {{
                    enabled: true,
                    type: 'curvedCW',
                    roundness: 0.2
                }},
                hoverWidth: 3
            }},
            physics: {{
                enabled: true,
                barnesHut: {{
                    gravitationalConstant: -2000,
                    centralGravity: 0.3,
                    springLength: 200,
                    springConstant: 0.001,
                    damping: 0.09,
                    avoidOverlap: 0.1
                }},
                stabilization: {{
                    enabled: true,
                    iterations: 1000,
                    updateInterval: 25,
                    onlyDynamicEdges: false,
                    fit: true
                }},
                maxVelocity: 50,
                minVelocity: 0.75,
                solver: 'barnesHut',
                timestep: 0.5
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 100,
                navigationButtons: true,
                keyboard: true
            }}
        }};

        // Initialize network
        console.log('Criando rede vis.js...');
        var network = new vis.Network(container, data, options);
        console.log('Rede criada com sucesso!');

        // Event de estabilização
        network.on("stabilizationProgress", function(params) {{
            var progress = Math.round((params.iterations / params.total) * 100);
            console.log('Estabilizando grafo:', progress + '%');
        }});

        network.on("stabilizationIterationsDone", function() {{
            console.log('Estabilização completa!');
            network.setOptions({{ physics: false }});
        }});

        network.on("startStabilizing", function() {{
            console.log('Iniciando estabilização...');
        }});

        // Toggle physics
        var physicsEnabled = false;
        function togglePhysics() {{
            physicsEnabled = !physicsEnabled;
            network.setOptions({{ physics: {{ enabled: physicsEnabled }} }});
            console.log('Física:', physicsEnabled ? 'LIGADA' : 'DESLIGADA');
        }}

        // Network events
        network.on("click", function (params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                console.log('Clicou no bairro:', nodeId);
            }}
        }});

        network.on("hoverNode", function (params) {{
            container.style.cursor = 'pointer';
        }});

        network.on("blurNode", function (params) {{
            container.style.cursor = 'default';
        }});

        // Funcionalidade de busca
        var searchInput = document.getElementById('search-input');
        var searchResults = document.getElementById('search-results');
        var allNodes = nodes.get();

        // Função para normalizar texto (remover acentos e converter para minúsculas)
        function normalizeText(text) {{
            return text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
        }}

        // Função para buscar bairros
        function searchNodes(query) {{
            if (!query || query.length < 2) {{
                searchResults.innerHTML = '';
                return;
            }}

            var normalizedQuery = normalizeText(query);
            var results = allNodes.filter(function(node) {{
                return normalizeText(node.label).includes(normalizedQuery);
            }});

            // Limitar a 10 resultados
            results = results.slice(0, 10);

            // Exibir resultados
            if (results.length > 0) {{
                searchResults.innerHTML = results.map(function(node) {{
                    return '<div class="search-result-item" onclick="focusNode(\'' + node.id + '\')">' +
                           '<span class="highlight-node">' + node.label + '</span><br>' +
                           '<small>Subregião: ' + node.title.split('Subregião: ')[1].split('<br>')[0] + '</small>' +
                           '</div>';
                }}).join('');
            }} else {{
                searchResults.innerHTML = '<div style="padding: 8px; color: #999;">Nenhum bairro encontrado</div>';
            }}
        }}

        // Função para focar em um nó específico
        function focusNode(nodeId) {{
            // Selecionar o nó
            network.selectNodes([nodeId]);

            // Focar no nó com animação
            network.focus(nodeId, {{
                scale: 2.0,
                animation: {{
                    duration: 1000,
                    easingFunction: 'easeInOutQuad'
                }}
            }});

            // Destacar temporariamente
            var originalColor = nodes.get(nodeId).color;
            nodes.update({{
                id: nodeId,
                color: {{
                    background: '#FFD700',
                    border: '#FF0000'
                }},
                borderWidth: 5
            }});

            // Restaurar cor original após 3 segundos
            setTimeout(function() {{
                nodes.update({{
                    id: nodeId,
                    color: originalColor,
                    borderWidth: 2
                }});
            }}, 3000);

            // Limpar campo de busca e resultados após seleção
            setTimeout(function() {{
                searchInput.value = '';
                searchResults.innerHTML = '';
            }}, 500);
        }}

        // Event listener para o input de busca
        searchInput.addEventListener('input', function() {{
            searchNodes(this.value);
        }});

        // Permitir Enter para selecionar primeiro resultado
        searchInput.addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                var firstResult = searchResults.querySelector('.search-result-item');
                if (firstResult) {{
                    firstResult.click();
                }}
            }}
        }});

        console.log('Grafo carregado com sucesso!');
        console.log('Vértices:', nodes.length, 'Arestas:', edges.length);
        console.log('Use a caixa de busca para encontrar bairros!');
    </script>
</body>
</html>
"""

    # Salvar arquivo
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"\n✓ Visualização interativa salva em: {arquivo_saida}")
    print(f"\nPara visualizar, abra o arquivo '{arquivo_saida}' em qualquer navegador!")
    print("Ou execute: xdg-open " + arquivo_saida)

    return arquivo_saida


def main():
    """Função principal"""
    # Construir o grafo
    grafo = construir_grafo_completo(
        '/mnt/c/Users/luise/Downloads/bairros_por_subregiao_limpo.xlsx',
        '/mnt/c/Users/luise/Downloads/Todas as vias FINAL (1).xlsx'
    )

    grafo.estatisticas()

    # Gerar visualização
    arquivo = gerar_html_interativo(grafo)

    print("\n" + "="*60)
    print("VISUALIZAÇÃO CRIADA COM SUCESSO!")
    print("="*60)


if __name__ == '__main__':
    main()
