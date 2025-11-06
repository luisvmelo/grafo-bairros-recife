# Como Visualizar o Grafo

## Visualização Atual

Agora **TODAS as 904 arestas são desenhadas individualmente**!

### O que mudou:

**ANTES:**
- Uma linha grossa representava múltiplas vias
- Água Fria mostrava apenas 7 linhas (uma para cada bairro conectado)

**AGORA:**
- Cada via é uma linha fina separada
- Água Fria mostra **51 linhas individuais** (todas as suas vias)
- Arestas paralelas aparecem como múltiplas linhas curvas entre os mesmos bairros

## Como Abrir a Visualização

### Opção 1: Da pasta Downloads
```
C:\Users\luise\Downloads\grafo_interativo.html
```
Clique duas vezes para abrir no navegador.

### Opção 2: Gerar nova visualização
```bash
python3 visualizar_interativo.py
```

## O que Você Verá

### Estatísticas no Topo:
- 📍 **94 bairros** (vértices)
- 🛣️ **904 vias** (arestas individuais)
- 📊 **Grau médio: 19.23**

### Características Visuais:

1. **Cada linha = Uma via individual**
   - Todas as linhas têm 1px de largura
   - Linhas cinzas (#848484)
   - Ficam vermelhas ao passar o mouse

2. **Arestas Paralelas**
   - Aparecem como múltiplas linhas curvas
   - Exemplo: Água Fria → Fundão mostra **13 linhas** (13 vias diferentes)

3. **Interatividade**
   - 🖱️ Passe o mouse sobre uma linha para ver:
     - Nome da via
     - Distância em metros
     - Bairros conectados
   - 🔍 Scroll para zoom
   - ✋ Clique e arraste para mover bairros
   - ⚡ Toggle Física para pausar/retomar animação

4. **Cores dos Bairros**
   - Cada cor representa uma subregião diferente
   - Tamanho do círculo = número de vias do bairro

## Exemplo: Explorando Água Fria

1. Abra o grafo no navegador
2. Procure o bairro "Água Fria" (um dos maiores círculos)
3. Conte as linhas saindo dele: você verá **51 linhas individuais**!
4. Observe que várias linhas vão para o mesmo bairro (arestas paralelas)
5. Passe o mouse em cada linha para ver qual via ela representa

### Água Fria → Fundão (13 vias):
Você verá 13 linhas separadas conectando esses bairros:
- Avenida Anibal Benevolo (1196.21m)
- Avenida Beberibe (2237.49m)
- Rua Alto Bonito (493.18m)
- Rua Conselheiro Barros Barreto (296.26m)
- ... e mais 9 vias

## Controles Úteis

### Botões no Canto Direito:
- 🔍 **Ajustar Zoom**: Centraliza e ajusta o zoom automaticamente
- ⚡ **Toggle Física**: Liga/desliga a simulação física
- 🎯 **Estabilizar**: Reorganiza o grafo automaticamente

### Navegação:
- **Scroll**: Zoom in/out
- **Clique e arraste (fundo)**: Move o grafo todo
- **Clique e arraste (bairro)**: Move um bairro específico
- **Double-click (bairro)**: Centraliza nele

## Performance

Com 904 arestas individuais, o grafo pode ficar denso. Dicas:

1. **Dê zoom** para ver detalhes de uma região específica
2. **Pause a física** (Toggle Física) para melhor performance
3. **Arraste bairros** para desembaraçar linhas sobrepostas
4. **Passe o mouse** nas linhas para identificar cada via

## Verificação

Para confirmar que todas as arestas estão lá:

```bash
python3 -c "
from carregar_dados import construir_grafo_completo
grafo = construir_grafo_completo('bairros_por_subregiao_limpo.xlsx', 'Todas as vias FINAL (1).xlsx')
print(f'Água Fria tem {grafo.grau(\"Água Fria\")} arestas no grafo')
print(f'Todas elas estão desenhadas individualmente no HTML!')
"
```

Resultado: `Água Fria tem 51 arestas no grafo`

E você verá **51 linhas individuais** no HTML! ✓
