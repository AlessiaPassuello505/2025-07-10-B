import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.DiGraph()
        self._idMapP={}

    def creaGrafo(self,categoria,d1,d2):
        self._graph.clear()
        nodi = DAO.getNodi(categoria)
        for n in nodi:
            self._idMapP[n.product_id] = n
            self._graph.add_node(n)

        archi = DAO.getArchi(categoria,d1,d2,self._idMapP)
        for a in archi:
            self._graph.add_edge(a.p1, a.p2, weight=float(a.peso))

    def getBest5(self):
        vendite = []
        for nodo in self._graph.nodes:
            # out_degree pesato (somma pesi archi uscenti)
            peso_uscenti = self._graph.out_degree(nodo, weight='weight')
            # in_degree pesato (somma pesi archi entranti)
            peso_entranti = self._graph.in_degree(nodo, weight='weight')

            influenza = peso_entranti - peso_uscenti
            vendite.append((nodo,influenza))


        vendite_ord = sorted(vendite, key=lambda x: x[1],reverse=True)
        best5=vendite_ord[:5]

        return best5

    def camminoPiuLungo(self, l, start, end):
        self._camminoOttimo = []
        self._lungh_max = 0

        #Recuperiamo i nodi reali dal grafo usando la mappa
        # Convertiamo l'input del dropdown in int per evitare il KeyError '61'
        start_node = self._idMapP[int(start)]
        end_node = self._idMapP[int(end)]
        # Inizializziamo il cammino parziale con l'OGGETTO nodo reale
        parziale = [start_node]
        # Avviamo la ricorsione passando il nodo di arrivo reale
        self._ricorsione(parziale, l, end_node)

        return self._camminoOttimo, self._lungh_max

    def _ricorsione(self, parziale, l, end_node):
        # Un cammino di 'l' archi contiene esattamente 'l + 1' nodi
        if len(parziale) == l + 1:
            # Controlliamo se l'ultimo nodo inserito è il traguardo
            if parziale[-1] == end_node:
                current_score = self._getScore(parziale)
                if current_score > self._lungh_max:
                    self._lungh_max = current_score
                    self._camminoOttimo = copy.deepcopy(parziale)
            return

        # Esploriamo i successori (vicini in uscita) dell'ultimo nodo nel cammino
        nodo_corrente = parziale[-1]

        for v in self._graph.successors(nodo_corrente):
            # Vincolo: Il vertice può entrare una volta sola nel percorso
            if v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale, l, end_node)
                # Passo indietro (Backtracking)
                parziale.pop()
    def _getScore(self, parziale):
        tot = 0
        for i in range(1, len(parziale)):
            tot += self._graph[parziale[i-1]][parziale[i]]["weight"]

        return tot

    def getNodi(self):
        return list(self._graph.nodes())

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategorie(self):
        return DAO.getCategorie()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)