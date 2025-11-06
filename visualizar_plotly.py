"""
Visualização do grafo usando Plotly (mais leve e confiável)
"""
import plotly.graph_objects as go
import random
from math import cos, sin, pi
from carregar_dados import construir_grafo_completo


def visualizar_grafo_plotly(grafo, arquivo_saida='grafo_plotly.html'):
    """
    Gera visualização interativa usando Plotly

    Args:
        grafo: Instância do grafo
        arquivo_saida: Nome do arquivo HTML de saída
    """
    print("Gerando visualização com Plotly...")

    # Posicionar vértices em círculo
    vertices = list(grafo.vertices.keys())
    n = len(vertices)

    posicoes = {}
    raio = 10
    for i, vertice in enumerate(vertices):
        angulo = 2 * pi * i / n
        x = raio * cos(angulo)
        y = raio * sin(angulo)
        posicoes[vertice] = (x, y)

    # Preparar dados das arestas
    edge_traces = []
    arestas_processadas = set()

    print(f"Desenhando {grafo.num_arestas * 2} arestas...")

    for origem in grafo.adjacencias:
        for aresta in grafo.adjacencias[origem]:
            # Criar ID único
            aresta_id = (origem, aresta.destino, aresta.nome_via, aresta.peso)
            aresta_reversa_id = (aresta.destino, origem, aresta.nome_via, aresta.peso)

            if aresta_id not in arestas_processadas and aresta_reversa_id not in arestas_processadas:
                x0, y0 = posicoes[origem]
                x1, y1 = posicoes[aresta.destino]

                # Criar uma linha para cada aresta
                edge_trace = go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode='lines',
                    line=dict(width=0.5, color='#888'),
                    hoverinfo='text',
                    text=f"{aresta.nome_via}<br>{aresta.peso:.2f}m",
                    showlegend=False
                )
                edge_traces.append(edge_trace)
                arestas_processadas.add(aresta_id)

    print(f"✓ {len(edge_traces)} arestas desenhadas")

    # Preparar dados dos vértices
    node_x = []
    node_y = []
    node_text = []
    node_size = []
    node_color = []

    # Cores por subregião
    cores_subregioes = {}
    subregioes_unicas = set(v.subregiao for v in grafo.vertices.values() if v.subregiao)

    for i, subregiao in enumerate(sorted(subregioes_unicas)):
        # Gerar cor baseada no índice
        hue = (i * 360 / len(subregioes_unicas)) % 360
        cores_subregioes[subregiao] = f'hsl({hue}, 70%, 50%)'

    for vertice_nome in vertices:
        x, y = posicoes[vertice_nome]
        node_x.append(x)
        node_y.append(y)

        vertice = grafo.obter_vertice(vertice_nome)
        grau = grafo.grau(vertice_nome)

        node_text.append(f"{vertice_nome}<br>Subregião: {vertice.subregiao}<br>Vias: {grau}")
        node_size.append(10 + grau * 0.5)  # Tamanho baseado no grau

        cor = cores_subregioes.get(vertice.subregiao, '#999')
        node_color.append(cor)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=[grafo.obter_vertice(v).nome for v in vertices],
        textposition="top center",
        textfont=dict(size=8),
        hoverinfo='text',
        hovertext=node_text,
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color='white')
        ),
        showlegend=False
    )

    # Criar figura
    fig = go.Figure(data=edge_traces + [node_trace])

    # Layout
    fig.update_layout(
        title=dict(
            text=f"Grafo de Bairros do Recife<br><sub>{grafo.num_vertices()} bairros, {len(edge_traces)} vias</sub>",
            x=0.5,
            xanchor='center'
        ),
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=80),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        width=1400,
        height=1000
    )

    # Salvar
    fig.write_html(arquivo_saida)
    print(f"✓ Visualização salva em: {arquivo_saida}")

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
    arquivo = visualizar_grafo_plotly(grafo)

    print("\n" + "="*60)
    print("VISUALIZAÇÃO CRIADA COM SUCESSO!")
    print("="*60)
    print(f"\nAbra o arquivo: {arquivo}")
    print("\nVantagens do Plotly:")
    print("- Mais leve e rápido")
    print("- Zoom e pan nativos")
    print("- Tooltip ao passar o mouse")
    print("- Funciona em qualquer navegador")


if __name__ == '__main__':
    main()
