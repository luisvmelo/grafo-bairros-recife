"""
Script para visualizar o grafo de bairros
"""
import matplotlib.pyplot as plt
import random
from math import cos, sin, pi
from carregar_dados import construir_grafo_completo


def visualizar_grafo_simples(grafo, titulo="Grafo de Bairros do Recife"):
    """
    Visualização simples do grafo usando matplotlib

    Args:
        grafo: Instância do grafo
        titulo: Título do gráfico
    """
    print("Gerando visualização do grafo...")

    # Criar figura
    fig, ax = plt.subplots(figsize=(20, 20))

    # Posicionar vértices em círculo
    vertices = list(grafo.vertices.keys())
    n = len(vertices)

    # Calcular posições dos vértices em círculo
    posicoes = {}
    raio = 10
    for i, vertice in enumerate(vertices):
        angulo = 2 * pi * i / n
        x = raio * cos(angulo)
        y = raio * sin(angulo)
        posicoes[vertice] = (x, y)

    # Desenhar arestas
    print("Desenhando arestas...")
    arestas_desenhadas = set()

    for origem in grafo.adjacencias:
        for aresta in grafo.adjacencias[origem]:
            # Evitar desenhar a mesma aresta duas vezes (grafo não direcionado)
            par = tuple(sorted([origem, aresta.destino]))

            if par not in arestas_desenhadas:
                x1, y1 = posicoes[origem]
                x2, y2 = posicoes[aresta.destino]

                # Desenhar linha
                ax.plot([x1, x2], [y1, y2], 'b-', alpha=0.1, linewidth=0.5)
                arestas_desenhadas.add(par)

    # Desenhar vértices
    print("Desenhando vértices...")
    for vertice, (x, y) in posicoes.items():
        # Tamanho do nó baseado no grau
        grau = grafo.grau(vertice)
        tamanho = 50 + grau * 5

        # Cor baseada na subregião
        v = grafo.obter_vertice(vertice)
        if v.subregiao:
            # Gerar cor baseada na subregião
            hash_cor = hash(v.subregiao)
            cor = f"#{hash_cor % 256:02x}{(hash_cor >> 8) % 256:02x}{(hash_cor >> 16) % 256:02x}"
        else:
            cor = 'gray'

        ax.scatter(x, y, s=tamanho, c=cor, alpha=0.7, edgecolors='black', linewidths=1)

    # Adicionar labels apenas para os vértices com maior grau
    print("Adicionando labels dos principais bairros...")
    vertices_ordenados = sorted(vertices, key=lambda v: grafo.grau(v), reverse=True)

    for vertice in vertices_ordenados[:15]:  # Top 15 bairros
        x, y = posicoes[vertice]
        ax.annotate(vertice, (x, y), fontsize=8, ha='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

    ax.set_title(titulo, fontsize=16, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')

    # Adicionar legenda
    info_text = f"Vértices: {grafo.num_vertices()}\nArestas: {grafo.num_arestas}\nGrau médio: {sum(grafo.grau(v) for v in vertices) / len(vertices):.2f}"
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
            fontsize=12, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()

    # Salvar
    arquivo_saida = 'grafo_bairros.png'
    plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
    print(f"\n✓ Visualização salva em: {arquivo_saida}")

    # Mostrar
    plt.show()


def visualizar_subgrafo(grafo, bairro_central, profundidade=1):
    """
    Visualiza um subgrafo centrado em um bairro específico

    Args:
        grafo: Instância do grafo
        bairro_central: Bairro central
        profundidade: Quantos níveis de vizinhos incluir
    """
    print(f"\nGerando visualização do subgrafo centrado em '{bairro_central}'...")

    if bairro_central not in grafo.vertices:
        print(f"Erro: Bairro '{bairro_central}' não encontrado no grafo")
        return

    # Encontrar vértices do subgrafo usando BFS simples
    vertices_subgrafo = {bairro_central}
    camada_atual = {bairro_central}

    for _ in range(profundidade):
        proxima_camada = set()
        for vertice in camada_atual:
            for aresta in grafo.obter_vizinhos(vertice):
                proxima_camada.add(aresta.destino)
        vertices_subgrafo.update(proxima_camada)
        camada_atual = proxima_camada

    # Criar figura
    fig, ax = plt.subplots(figsize=(15, 15))

    # Posicionar vértices em círculo
    vertices = list(vertices_subgrafo)
    n = len(vertices)

    posicoes = {}
    raio = 5

    # Colocar bairro central no meio
    posicoes[bairro_central] = (0, 0)

    # Outros vértices em círculo
    outros = [v for v in vertices if v != bairro_central]
    for i, vertice in enumerate(outros):
        angulo = 2 * pi * i / len(outros)
        x = raio * cos(angulo)
        y = raio * sin(angulo)
        posicoes[vertice] = (x, y)

    # Desenhar arestas do subgrafo
    arestas_desenhadas = set()

    for origem in vertices_subgrafo:
        for aresta in grafo.obter_vizinhos(origem):
            if aresta.destino in vertices_subgrafo:
                par = tuple(sorted([origem, aresta.destino]))

                if par not in arestas_desenhadas:
                    x1, y1 = posicoes[origem]
                    x2, y2 = posicoes[aresta.destino]

                    # Cor da aresta baseada no peso (distância)
                    peso = aresta.peso
                    if peso < 500:
                        cor = 'green'
                        alpha = 0.6
                    elif peso < 1500:
                        cor = 'orange'
                        alpha = 0.5
                    else:
                        cor = 'red'
                        alpha = 0.4

                    ax.plot([x1, x2], [y1, y2], color=cor, alpha=alpha, linewidth=2)
                    arestas_desenhadas.add(par)

    # Desenhar vértices
    for vertice in vertices_subgrafo:
        x, y = posicoes[vertice]

        if vertice == bairro_central:
            # Destaque para o bairro central
            ax.scatter(x, y, s=800, c='red', alpha=0.9, edgecolors='black', linewidths=3)
        else:
            grau_local = sum(1 for a in grafo.obter_vizinhos(vertice) if a.destino in vertices_subgrafo)
            tamanho = 300 + grau_local * 50
            ax.scatter(x, y, s=tamanho, c='lightblue', alpha=0.7, edgecolors='black', linewidths=2)

        # Label para todos os vértices (subgrafo pequeno)
        ax.annotate(vertice, (x, y), fontsize=10, ha='center', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))

    ax.set_title(f"Subgrafo: Vizinhança de '{bairro_central}'", fontsize=16, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')

    # Legenda de cores
    legend_text = "Distância das vias:\n🟢 < 500m\n🟠 500-1500m\n🔴 > 1500m"
    ax.text(0.02, 0.98, legend_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    plt.tight_layout()

    # Salvar
    arquivo_saida = f'subgrafo_{bairro_central.replace(" ", "_")}.png'
    plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
    print(f"✓ Visualização salva em: {arquivo_saida}")

    plt.show()


def main():
    """Função principal"""
    # Construir o grafo
    grafo = construir_grafo_completo(
        '/mnt/c/Users/luise/Downloads/bairros_por_subregiao_limpo.xlsx',
        '/mnt/c/Users/luise/Downloads/Todas as vias FINAL (1).xlsx'
    )

    print("\n" + "="*60)
    print("OPÇÕES DE VISUALIZAÇÃO")
    print("="*60)
    print("1. Visualizar grafo completo")
    print("2. Visualizar subgrafo (vizinhança de um bairro)")
    print("="*60)

    opcao = input("\nEscolha uma opção (1 ou 2): ").strip()

    if opcao == "1":
        visualizar_grafo_simples(grafo)

    elif opcao == "2":
        print("\nBairros disponíveis (primeiros 20):")
        bairros = grafo.listar_vertices()[:20]
        for i, bairro in enumerate(bairros, 1):
            print(f"{i}. {bairro}")
        print("...")

        bairro = input("\nDigite o nome do bairro central: ").strip()
        profundidade = input("Digite a profundidade (1-3, padrão 1): ").strip()

        if not profundidade:
            profundidade = 1
        else:
            profundidade = int(profundidade)

        visualizar_subgrafo(grafo, bairro, profundidade)

    else:
        print("Opção inválida!")


if __name__ == '__main__':
    main()
