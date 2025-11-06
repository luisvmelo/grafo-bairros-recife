"""
Script principal para construir e testar o grafo de bairros
"""
import argparse
from carregar_dados import construir_grafo_completo


def main():
    """Função principal"""

    parser = argparse.ArgumentParser(description='Construir grafo de bairros do Recife')
    parser.add_argument(
        '--subregioes',
        type=str,
        default='/mnt/c/Users/luise/Downloads/bairros_por_subregiao_limpo.xlsx',
        help='Caminho para planilha de bairros por subregião'
    )
    parser.add_argument(
        '--vias',
        type=str,
        default='/mnt/c/Users/luise/Downloads/Todas as vias FINAL (1).xlsx',
        help='Caminho para planilha de vias'
    )

    args = parser.parse_args()

    # Construir o grafo
    grafo = construir_grafo_completo(args.subregioes, args.vias)

    # Exibir estatísticas
    grafo.estatisticas()

    # Exemplos de uso do grafo
    print("="*60)
    print("EXEMPLOS DE USO DO GRAFO")
    print("="*60)

    # Exemplo 1: Informações sobre um bairro específico
    bairro_exemplo = "Água Fria"
    print(f"\n1. Informações sobre o bairro '{bairro_exemplo}':")
    vertice = grafo.obter_vertice(bairro_exemplo)
    if vertice:
        print(f"   Nome: {vertice.nome}")
        print(f"   Subregião: {vertice.subregiao}")
        print(f"   Grau (conexões): {grafo.grau(bairro_exemplo)}")

        # Listar algumas conexões
        vizinhos = grafo.obter_vizinhos(bairro_exemplo)
        print(f"\n   Primeiras 5 conexões:")
        for i, aresta in enumerate(vizinhos[:5]):
            print(f"   {i+1}. {aresta.destino} via {aresta.nome_via} ({aresta.peso:.2f}m)")

    # Exemplo 2: Arestas paralelas entre dois bairros
    bairro1 = "Água Fria"
    bairro2 = "Beberibe"
    print(f"\n2. Vias entre '{bairro1}' e '{bairro2}':")
    arestas = grafo.obter_arestas_entre(bairro1, bairro2)
    if arestas:
        for i, aresta in enumerate(arestas):
            print(f"   {i+1}. {aresta.nome_via} - {aresta.peso:.2f}m")
    else:
        print(f"   Não há conexão direta entre esses bairros")

    # Exemplo 3: Listar alguns bairros
    print(f"\n3. Primeiros 10 bairros no grafo:")
    bairros = grafo.listar_vertices()[:10]
    for i, bairro in enumerate(bairros):
        v = grafo.obter_vertice(bairro)
        print(f"   {i+1}. {bairro} (Subregião: {v.subregiao})")

    print("\n" + "="*60)
    print("GRAFO PRONTO PARA USO!")
    print("="*60 + "\n")

    return grafo


if __name__ == '__main__':
    grafo = main()
