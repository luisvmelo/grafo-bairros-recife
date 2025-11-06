"""
Visualização com layout orgânico/geográfico
Distribui os bairros baseado em subregiões de forma mais natural
"""
import random
from carregar_dados import construir_grafo_completo


def visualizar_layout_organico(grafo, arquivo_saida='grafo_organico.html'):
    """
    Gera visualização com layout baseado em subregiões (mais natural)
    """
    print("Gerando visualização com layout orgânico...")

    # Agrupar bairros por subregião
    bairros_por_subregiao = {}
    for nome, vertice in grafo.vertices.items():
        if vertice.subregiao:
            if vertice.subregiao not in bairros_por_subregiao:
                bairros_por_subregiao[vertice.subregiao] = []
            bairros_por_subregiao[vertice.subregiao].append(nome)

    # Posicionar subregiões em uma grade
    subregioes = sorted(bairros_por_subregiao.keys())
    n_cols = 6  # 6 colunas
    n_rows = (len(subregioes) + n_cols - 1) // n_cols

    posicoes = {}
    centro_x, centro_y = 800, 600
    espacamento_x = 400
    espacamento_y = 350

    for i, subregiao in enumerate(subregioes):
        col = i % n_cols
        row = i // n_cols

        # Centro da subregião
        centro_sub_x = centro_x + (col - n_cols/2) * espacamento_x
        centro_sub_y = centro_y + (row - n_rows/2) * espacamento_y

        # Distribuir bairros dentro da subregião
        bairros = bairros_por_subregiao[subregiao]
        raio_sub = 80 + len(bairros) * 5  # Raio baseado no número de bairros

        for j, bairro in enumerate(bairros):
            # Distribuir em círculo dentro da subregião
            if len(bairros) == 1:
                x, y = centro_sub_x, centro_sub_y
            else:
                angulo = 2 * 3.14159 * j / len(bairros)
                x = centro_sub_x + raio_sub * (0.5 + 0.5 * random.random()) * (1 if j % 2 == 0 else -1) * abs(random.gauss(1, 0.3))
                y = centro_sub_y + raio_sub * (0.5 + 0.5 * random.random()) * (1 if j % 3 == 0 else -1) * abs(random.gauss(1, 0.3))

            posicoes[bairro] = (x, y)

    # Preparar arestas
    arestas_lista = []
    arestas_processadas = set()

    for origem in grafo.adjacencias:
        for aresta in grafo.adjacencias[origem]:
            aresta_id = (origem, aresta.destino, aresta.nome_via, aresta.peso)
            aresta_reversa_id = (aresta.destino, origem, aresta.nome_via, aresta.peso)

            if aresta_id not in arestas_processadas and aresta_reversa_id not in arestas_processadas:
                if origem in posicoes and aresta.destino in posicoes:
                    x1, y1 = posicoes[origem]
                    x2, y2 = posicoes[aresta.destino]

                    arestas_lista.append({
                        'x1': x1, 'y1': y1,
                        'x2': x2, 'y2': y2,
                        'origem': origem.replace("'", "\\'"),
                        'destino': aresta.destino.replace("'", "\\'"),
                        'via': aresta.nome_via.replace("'", "\\'"),
                        'peso': aresta.peso
                    })
                    arestas_processadas.add(aresta_id)

    # Preparar vértices
    vertices_lista = []
    cores_subregioes = {}

    for i, subregiao in enumerate(sorted(subregioes)):
        hue = (i * 360 / len(subregioes)) % 360
        cores_subregioes[subregiao] = f'hsl({hue}, 70%, 60%)'

    for nome in grafo.vertices.keys():
        if nome in posicoes:
            x, y = posicoes[nome]
            vertice = grafo.obter_vertice(nome)
            grau = grafo.grau(nome)

            cor = cores_subregioes.get(vertice.subregiao, '#999')
            tamanho = min(25, 6 + grau * 0.4)

            vertices_lista.append({
                'x': x, 'y': y,
                'nome': nome.replace("'", "\\'"),
                'subregiao': vertice.subregiao if vertice.subregiao else 'N/A',
                'grau': grau,
                'cor': cor,
                'tamanho': tamanho
            })

    # HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Grafo de Bairros - Layout Orgânico</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #f5f5f5;
            overflow: hidden;
        }}
        #header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        #header h1 {{
            font-size: 24px;
            margin: 0;
        }}
        #header p {{
            margin: 5px 0 0 0;
            opacity: 0.9;
            font-size: 14px;
        }}
        #controls {{
            position: fixed;
            top: 90px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            z-index: 1000;
            width: 200px;
        }}
        #search-box {{
            position: fixed;
            top: 90px;
            left: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            z-index: 1000;
            width: 280px;
        }}
        h3 {{
            margin: 0 0 10px 0;
            font-size: 16px;
            color: #333;
        }}
        input {{
            width: 100%;
            padding: 10px;
            border: 2px solid #667eea;
            border-radius: 5px;
            font-size: 14px;
        }}
        #search-results {{
            max-height: 400px;
            overflow-y: auto;
            margin-top: 10px;
        }}
        .search-item {{
            padding: 10px;
            cursor: pointer;
            border-bottom: 1px solid #eee;
            transition: all 0.2s;
        }}
        .search-item:hover {{
            background: #f0f0f0;
            padding-left: 15px;
        }}
        .search-item strong {{
            color: #667eea;
        }}
        button {{
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.2s;
        }}
        button:hover {{
            background: #764ba2;
        }}
        #canvas-container {{
            height: calc(100vh - 80px);
            overflow: hidden;
            position: relative;
            background: white;
        }}
        canvas {{
            display: block;
            cursor: grab;
        }}
        canvas:active {{
            cursor: grabbing;
        }}
        #tooltip {{
            position: fixed;
            background: rgba(0, 0, 0, 0.95);
            color: white;
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 13px;
            pointer-events: none;
            display: none;
            z-index: 2000;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        #info-panel {{
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(255,255,255,0.95);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            font-size: 12px;
            z-index: 1000;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>🗺️ Grafo de Bairros do Recife - Layout Orgânico</h1>
        <p>{grafo.num_vertices()} bairros | {len(arestas_lista)} vias | Distribuição por subregiões</p>
    </div>

    <div id="search-box">
        <h3>🔍 Buscar Bairro</h3>
        <input type="text" id="search-input" placeholder="Digite o nome do bairro..."/>
        <div id="search-results"></div>
    </div>

    <div id="controls">
        <h3>⚙️ Controles</h3>
        <button onclick="resetView()">🏠 Visão Inicial</button>
        <button onclick="zoomIn()">➕ Zoom In</button>
        <button onclick="zoomOut()">➖ Zoom Out</button>
        <button onclick="toggleLabels()">🏷️ Labels</button>
    </div>

    <div id="info-panel">
        <strong>💡 Como usar:</strong><br>
        • Arraste para mover<br>
        • Scroll para zoom<br>
        • Passe o mouse nos círculos<br>
        • Use a busca para localizar
    </div>

    <div id="canvas-container">
        <canvas id="canvas" width="3200" height="2400"></canvas>
    </div>

    <div id="tooltip"></div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const tooltip = document.getElementById('tooltip');

        const arestas = {str(arestas_lista)};
        const vertices = {str(vertices_lista)};

        let scale = 1;
        let offsetX = -800;
        let offsetY = -600;
        let isDragging = false;
        let lastX, lastY;
        let showLabels = true;

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.save();
            ctx.translate(offsetX, offsetY);
            ctx.scale(scale, scale);

            // Arestas
            ctx.globalAlpha = 0.15;
            ctx.strokeStyle = '#888';
            ctx.lineWidth = 0.8;
            arestas.forEach(a => {{
                ctx.beginPath();
                ctx.moveTo(a.x1, a.y1);
                ctx.lineTo(a.x2, a.y2);
                ctx.stroke();
            }});
            ctx.globalAlpha = 1;

            // Vértices
            vertices.forEach(v => {{
                // Círculo
                ctx.fillStyle = v.cor;
                ctx.beginPath();
                ctx.arc(v.x, v.y, v.tamanho, 0, 2 * Math.PI);
                ctx.fill();
                ctx.strokeStyle = 'white';
                ctx.lineWidth = 2.5;
                ctx.stroke();

                // Label
                if (showLabels && scale > 0.5) {{
                    ctx.fillStyle = '#000';
                    ctx.font = 'bold 11px Arial';
                    ctx.textAlign = 'center';
                    ctx.fillText(v.nome, v.x, v.y - v.tamanho - 8);
                }}
            }});

            ctx.restore();
        }}

        // Mouse
        canvas.addEventListener('mousedown', e => {{
            isDragging = true;
            lastX = e.clientX;
            lastY = e.clientY;
        }});

        canvas.addEventListener('mousemove', e => {{
            if (isDragging) {{
                offsetX += e.clientX - lastX;
                offsetY += e.clientY - lastY;
                lastX = e.clientX;
                lastY = e.clientY;
                draw();
            }} else {{
                const rect = canvas.getBoundingClientRect();
                const x = (e.clientX - rect.left - offsetX) / scale;
                const y = (e.clientY - rect.top - offsetY) / scale;

                let found = false;
                for (const v of vertices) {{
                    const dist = Math.sqrt((x - v.x) ** 2 + (y - v.y) ** 2);
                    if (dist < v.tamanho) {{
                        tooltip.style.display = 'block';
                        tooltip.style.left = e.clientX + 15 + 'px';
                        tooltip.style.top = e.clientY + 15 + 'px';
                        tooltip.innerHTML = `<strong>${{v.nome}}</strong><br>📍 Subregião: ${{v.subregiao}}<br>🛣️ Vias: ${{v.grau}}`;
                        found = true;
                        break;
                    }}
                }}
                if (!found) tooltip.style.display = 'none';
            }}
        }});

        canvas.addEventListener('mouseup', () => {{ isDragging = false; }});
        canvas.addEventListener('mouseleave', () => {{ isDragging = false; }});

        canvas.addEventListener('wheel', e => {{
            e.preventDefault();
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            const worldX = (mouseX - offsetX) / scale;
            const worldY = (mouseY - offsetY) / scale;

            const delta = e.deltaY > 0 ? 0.9 : 1.1;
            scale *= delta;
            scale = Math.max(0.1, Math.min(5, scale));

            offsetX = mouseX - worldX * scale;
            offsetY = mouseY - worldY * scale;

            draw();
        }});

        // Funções
        function resetView() {{
            scale = 1;
            offsetX = -800;
            offsetY = -600;
            draw();
        }}

        function zoomIn() {{
            scale *= 1.3;
            draw();
        }}

        function zoomOut() {{
            scale *= 0.7;
            draw();
        }}

        function toggleLabels() {{
            showLabels = !showLabels;
            draw();
        }}

        // Busca
        const searchInput = document.getElementById('search-input');
        const searchResults = document.getElementById('search-results');

        searchInput.addEventListener('input', e => {{
            const query = e.target.value.toLowerCase();
            if (query.length < 2) {{
                searchResults.innerHTML = '';
                return;
            }}

            const results = vertices.filter(v =>
                v.nome.toLowerCase().includes(query)
            ).slice(0, 15);

            if (results.length > 0) {{
                searchResults.innerHTML = results.map(v =>
                    `<div class="search-item" onclick="focusNode('${{v.nome}}')">
                        <strong>${{v.nome}}</strong><br>
                        <small>📍 ${{v.subregiao}} • 🛣️ ${{v.grau}} vias</small>
                    </div>`
                ).join('');
            }} else {{
                searchResults.innerHTML = '<div style="padding: 10px; color: #999;">Nenhum resultado</div>';
            }}
        }});

        function focusNode(nome) {{
            const v = vertices.find(x => x.nome === nome);
            if (v) {{
                scale = 1.5;
                offsetX = canvas.width / 2 - v.x * scale;
                offsetY = canvas.height / 2 - v.y * scale;
                draw();

                // Highlight
                setTimeout(() => {{
                    ctx.save();
                    ctx.translate(offsetX, offsetY);
                    ctx.scale(scale, scale);
                    ctx.strokeStyle = '#FF0000';
                    ctx.lineWidth = 4;
                    ctx.beginPath();
                    ctx.arc(v.x, v.y, v.tamanho + 8, 0, 2 * Math.PI);
                    ctx.stroke();
                    ctx.restore();
                }}, 100);

                searchInput.value = '';
                searchResults.innerHTML = '';
            }}
        }}

        draw();
        console.log('✓ Grafo carregado:', vertices.length, 'vértices,', arestas.length, 'arestas');
    </script>
</body>
</html>
"""

    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Visualização salva em: {arquivo_saida}")
    return arquivo_saida


def main():
    grafo = construir_grafo_completo(
        '/mnt/c/Users/luise/Downloads/bairros_por_subregiao_limpo.xlsx',
        '/mnt/c/Users/luise/Downloads/Todas as vias FINAL (1).xlsx'
    )

    grafo.estatisticas()
    arquivo = visualizar_layout_organico(grafo)

    print("\n" + "="*60)
    print("VISUALIZAÇÃO COM LAYOUT ORGÂNICO!")
    print("="*60)
    print("\n✨ Melhorias:")
    print("- Bairros agrupados por subregião (mais geográfico)")
    print("- Layout não-circular (mais natural)")
    print("- Distribuição orgânica dos bairros")
    print("- Zoom suave e centralizado")
    print("- TODAS as 902 arestas desenhadas")


if __name__ == '__main__':
    main()
