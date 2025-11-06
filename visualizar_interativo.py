"""
Visualização interativa do grafo usando HTML
(Não requer bibliotecas externas além de pandas)
"""
import json
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

    # Preparar dados das arestas
    # Primeiro, contar quantas arestas paralelas existem entre cada par de bairros
    arestas_por_par = {}

    for origem in grafo.adjacencias:
        for aresta in grafo.adjacencias[origem]:
            par = tuple(sorted([origem, aresta.destino]))

            if par not in arestas_por_par:
                arestas_por_par[par] = []

            arestas_por_par[par].append(aresta)

    # Agora criar as arestas para visualização
    arestas = []
    total_arestas_reais = 0

    for par, lista_arestas in arestas_por_par.items():
        origem, destino = par
        num_vias = len(lista_arestas)
        total_arestas_reais += num_vias

        # Pegar a via mais curta como referência
        via_mais_curta = min(lista_arestas, key=lambda a: a.peso)

        # Largura proporcional ao número de vias paralelas
        largura = min(15, 1 + num_vias * 0.5)

        # Criar título com todas as vias
        if num_vias == 1:
            titulo = f"{via_mais_curta.nome_via}<br>{via_mais_curta.peso:.2f}m"
        else:
            titulo = f"<b>{num_vias} vias conectando esses bairros:</b><br>"
            for a in lista_arestas[:5]:  # Mostrar até 5 vias
                titulo += f"• {a.nome_via} ({a.peso:.2f}m)<br>"
            if num_vias > 5:
                titulo += f"... e mais {num_vias - 5} vias"

        # Label para mostrar número de vias se houver múltiplas
        label = str(num_vias) if num_vias > 1 else ''

        arestas.append({
            'from': origem,
            'to': destino,
            'title': titulo,
            'width': largura,
            'length': min(300, via_mais_curta.peso / 5),
            'label': label
        })

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
    </style>
</head>
<body>
    <div id="header">
        <h1>🗺️ Grafo de Bairros do Recife</h1>
        <p>Visualização Interativa das Conexões entre Bairros</p>
    </div>

    <div id="info">
        <span class="stats">📍 Vértices (Bairros): {grafo.num_vertices()}</span>
        <span class="stats">🛣️ Vias Totais: {total_arestas_reais}</span>
        <span class="stats">🔗 Conexões Únicas: {len(arestas)}</span>
        <span class="stats">📊 Grau Médio: {sum(grafo.grau(v) for v in grafo.vertices) / len(grafo.vertices):.2f}</span>
    </div>

    <div id="controls">
        <h3 style="margin-top: 0;">Controles</h3>
        <button onclick="network.fit()">🔍 Ajustar Zoom</button>
        <button onclick="togglePhysics()">⚡ Toggle Física</button>
        <button onclick="network.stabilize()">🎯 Estabilizar</button>
    </div>

    <div id="legend">
        <div class="legend-title">📌 Legenda</div>
        <div class="legend-item">• <b>Tamanho do nó</b> = Número de vias do bairro</div>
        <div class="legend-item">• <b>Cor do nó</b> = Subregião do bairro</div>
        <div class="legend-item">• <b>Espessura da linha</b> = Número de vias paralelas</div>
        <div class="legend-item">• <b>Número na linha</b> = Quantidade de vias entre os bairros</div>
        <div class="legend-item">• <b>Passe o mouse</b> para ver todas as vias</div>
        <div class="legend-item">• <b>Clique e arraste</b> para mover</div>
        <div class="legend-item">• <b>Scroll</b> para zoom</div>
    </div>

    <div id="mynetwork"></div>

    <script type="text/javascript">
        // Dados
        var nodes = new vis.DataSet({json.dumps(nos, ensure_ascii=False)});
        var edges = new vis.DataSet({json.dumps(arestas, ensure_ascii=False)});

        // Container
        var container = document.getElementById('mynetwork');

        // Data
        var data = {{
            nodes: nodes,
            edges: edges
        }};

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
                color: {{
                    color: '#848484',
                    highlight: '#FF0000',
                    hover: '#FF0000'
                }},
                smooth: {{
                    enabled: true,
                    type: 'continuous'
                }},
                hoverWidth: 2,
                font: {{
                    size: 14,
                    color: '#FF0000',
                    face: 'Arial',
                    background: 'white',
                    strokeWidth: 0,
                    align: 'middle'
                }}
            }},
            physics: {{
                enabled: true,
                barnesHut: {{
                    gravitationalConstant: -8000,
                    centralGravity: 0.3,
                    springLength: 150,
                    springConstant: 0.04,
                    damping: 0.09
                }},
                stabilization: {{
                    iterations: 150
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 100,
                navigationButtons: true,
                keyboard: true
            }}
        }};

        // Initialize network
        var network = new vis.Network(container, data, options);

        // Toggle physics
        var physicsEnabled = true;
        function togglePhysics() {{
            physicsEnabled = !physicsEnabled;
            network.setOptions({{ physics: {{ enabled: physicsEnabled }} }});
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

        console.log('Grafo carregado com sucesso!');
        console.log('Vértices:', nodes.length, 'Arestas:', edges.length);
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
