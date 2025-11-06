"""
Implementação de um Grafo não direcionado com arestas paralelas
para representar bairros e suas conexões através de vias
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from collections import defaultdict


@dataclass
class Aresta:
    """Representa uma aresta do grafo"""
    origem: str
    destino: str
    nome_via: str
    peso: float

    def __repr__(self):
        return f"Aresta({self.origem} -> {self.destino}, via: {self.nome_via}, peso: {self.peso})"


@dataclass
class Vertice:
    """Representa um vértice (bairro) do grafo"""
    nome: str
    subregiao: Optional[str] = None

    def __repr__(self):
        return f"Vertice({self.nome}, subregiao: {self.subregiao})"

    def __hash__(self):
        return hash(self.nome)

    def __eq__(self, other):
        if isinstance(other, Vertice):
            return self.nome == other.nome
        return False


class Grafo:
    """
    Grafo não direcionado com suporte a arestas paralelas
    """

    def __init__(self):
        self.vertices: Dict[str, Vertice] = {}
        # Lista de adjacências: cada vértice mapeia para uma lista de arestas
        self.adjacencias: Dict[str, List[Aresta]] = defaultdict(list)
        self.num_arestas = 0

    def adicionar_vertice(self, nome: str, subregiao: Optional[str] = None) -> Vertice:
        """Adiciona um vértice ao grafo"""
        nome_normalizado = nome.strip()

        if nome_normalizado not in self.vertices:
            vertice = Vertice(nome_normalizado, subregiao)
            self.vertices[nome_normalizado] = vertice
        else:
            # Atualiza subregião se fornecida
            if subregiao:
                self.vertices[nome_normalizado].subregiao = subregiao

        return self.vertices[nome_normalizado]

    def adicionar_aresta(self, origem: str, destino: str, nome_via: str, peso: float):
        """Adiciona uma aresta ao grafo (não direcionado, então adiciona em ambas as direções)"""
        origem_norm = origem.strip()
        destino_norm = destino.strip()

        # Garante que os vértices existem
        if origem_norm not in self.vertices:
            self.adicionar_vertice(origem_norm)
        if destino_norm not in self.vertices:
            self.adicionar_vertice(destino_norm)

        # Cria a aresta
        aresta = Aresta(origem_norm, destino_norm, nome_via.strip(), peso)

        # Adiciona nas adjacências (grafo não direcionado)
        self.adjacencias[origem_norm].append(aresta)

        # Adiciona a aresta reversa
        aresta_reversa = Aresta(destino_norm, origem_norm, nome_via.strip(), peso)
        self.adjacencias[destino_norm].append(aresta_reversa)

        self.num_arestas += 1

    def obter_vizinhos(self, vertice: str) -> List[Aresta]:
        """Retorna todas as arestas que saem de um vértice"""
        return self.adjacencias.get(vertice, [])

    def obter_vertice(self, nome: str) -> Optional[Vertice]:
        """Retorna um vértice pelo nome"""
        return self.vertices.get(nome)

    def grau(self, vertice: str) -> int:
        """Retorna o grau de um vértice (número de arestas incidentes)"""
        return len(self.adjacencias.get(vertice, []))

    def existe_aresta(self, origem: str, destino: str) -> bool:
        """Verifica se existe pelo menos uma aresta entre dois vértices"""
        if origem not in self.adjacencias:
            return False

        for aresta in self.adjacencias[origem]:
            if aresta.destino == destino:
                return True
        return False

    def obter_arestas_entre(self, origem: str, destino: str) -> List[Aresta]:
        """Retorna todas as arestas entre dois vértices (arestas paralelas)"""
        if origem not in self.adjacencias:
            return []

        arestas = []
        for aresta in self.adjacencias[origem]:
            if aresta.destino == destino:
                arestas.append(aresta)

        return arestas

    def num_vertices(self) -> int:
        """Retorna o número de vértices do grafo"""
        return len(self.vertices)

    def listar_vertices(self) -> List[str]:
        """Retorna lista com nomes de todos os vértices"""
        return list(self.vertices.keys())

    def __repr__(self):
        return f"Grafo(vertices={self.num_vertices()}, arestas={self.num_arestas})"

    def estatisticas(self):
        """Exibe estatísticas do grafo"""
        print(f"\n{'='*60}")
        print(f"ESTATÍSTICAS DO GRAFO")
        print(f"{'='*60}")
        print(f"Número de vértices (bairros): {self.num_vertices()}")
        print(f"Número de arestas (vias): {self.num_arestas}")

        # Grau médio
        if self.num_vertices() > 0:
            grau_total = sum(self.grau(v) for v in self.vertices)
            grau_medio = grau_total / self.num_vertices()
            print(f"Grau médio: {grau_medio:.2f}")

        # Vértice com maior grau
        if self.vertices:
            max_vertice = max(self.vertices.keys(), key=lambda v: self.grau(v))
            print(f"Bairro com mais conexões: {max_vertice} (grau: {self.grau(max_vertice)})")

        # Subregiões
        subregioes = set()
        for v in self.vertices.values():
            if v.subregiao:
                subregioes.add(v.subregiao)
        print(f"Número de subregiões: {len(subregioes)}")

        print(f"{'='*60}\n")
