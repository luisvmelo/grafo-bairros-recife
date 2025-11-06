"""
Funções para carregar dados das planilhas Excel e construir o grafo
"""
import pandas as pd
from grafo import Grafo


def carregar_vertices_subregioes(grafo: Grafo, caminho_planilha: str):
    """
    Carrega os vértices (bairros) da planilha de subregiões

    Args:
        grafo: Instância do grafo onde os vértices serão adicionados
        caminho_planilha: Caminho para a planilha de bairros por subregião
    """
    print(f"Carregando vértices de: {caminho_planilha}")

    df = pd.read_excel(caminho_planilha)

    vertices_adicionados = 0

    # Itera por cada coluna (cada coluna é uma subregião)
    for coluna in df.columns:
        subregiao = coluna

        # Itera por cada célula da coluna (cada célula é um bairro)
        for bairro in df[coluna].dropna():
            bairro_nome = str(bairro).strip()

            if bairro_nome:
                grafo.adicionar_vertice(bairro_nome, subregiao)
                vertices_adicionados += 1

    print(f"✓ {vertices_adicionados} vértices adicionados")
    return vertices_adicionados


def carregar_arestas_vias(grafo: Grafo, caminho_planilha: str):
    """
    Carrega as arestas (vias) da planilha principal

    Args:
        grafo: Instância do grafo onde as arestas serão adicionadas
        caminho_planilha: Caminho para a planilha de vias
    """
    print(f"Carregando arestas de: {caminho_planilha}")

    df = pd.read_excel(caminho_planilha)

    # Verifica se as colunas necessárias existem
    colunas_necessarias = ['bairro_origem', 'bairro_destino', 'nome_logradouro', 'distancia_metros']
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            raise ValueError(f"Coluna '{coluna}' não encontrada na planilha")

    arestas_adicionadas = 0

    # Itera por cada linha da planilha
    for _, row in df.iterrows():
        origem = str(row['bairro_origem']).strip()
        destino = str(row['bairro_destino']).strip()
        nome_via = str(row['nome_logradouro']).strip()
        peso = float(row['distancia_metros'])

        # Adiciona a aresta
        grafo.adicionar_aresta(origem, destino, nome_via, peso)
        arestas_adicionadas += 1

    print(f"✓ {arestas_adicionadas} arestas adicionadas")
    return arestas_adicionadas


def construir_grafo_completo(caminho_subregioes: str, caminho_vias: str) -> Grafo:
    """
    Constrói o grafo completo a partir das duas planilhas

    Args:
        caminho_subregioes: Caminho para a planilha de bairros por subregião
        caminho_vias: Caminho para a planilha de vias

    Returns:
        Grafo construído
    """
    print("\n" + "="*60)
    print("CONSTRUINDO GRAFO DE BAIRROS")
    print("="*60 + "\n")

    grafo = Grafo()

    # Passo 1: Carregar vértices (bairros com suas subregiões)
    print("Passo 1: Carregando vértices (bairros)...")
    carregar_vertices_subregioes(grafo, caminho_subregioes)

    # Passo 2: Carregar arestas (vias entre bairros)
    print("\nPasso 2: Carregando arestas (vias)...")
    carregar_arestas_vias(grafo, caminho_vias)

    print("\n" + "="*60)
    print("GRAFO CONSTRUÍDO COM SUCESSO!")
    print("="*60)

    return grafo
