import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._catScelta=None

    def fillDDCategorie(self):
        categorie = self._model.getCategorie()
        categorieDDI = list(map(lambda x: ft.dropdown.Option(x, on_click=self._choiceCategoria), categorie))
        self._view._ddcategory.options = categorieDDI
        self._view.update_page()

    def _choiceCategoria(self,e):
        self._catScelta=e.control.data

    def fillDDNodi(self):
        self._view._ddProdStart.options.clear()
        self._view._ddProdEnd.options.clear()

        nodi = self._model.getNodi()
        for n in nodi:
            self._view._ddProdStart.options.append(ft.dropdown.Option(key=str(n.product_id), text=str(n.product_name)))
            self._view._ddProdEnd.options.append(ft.dropdown.Option(key=str(n.product_id), text=str(n.product_name)))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        categoria = self._view._ddcategory.value
        data1=self._view._dp1.value
        data2=self._view._dp2.value
        self._view.txt_result.controls.append(ft.Text("Date selezionate:"))
        self._view.txt_result.controls.append(ft.Text(f"Start date: {data1}"))
        self._view.txt_result.controls.append(ft.Text(f"End date: {data2}"))

        if categoria is None or data1 is None or data2 is None:
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, selezionare un range di date e una categoria"))
            self._view.update_page()
            return
        self._model.creaGrafo(categoria,data1,data2)
        n, m = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato! ", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {m}"))

        self.fillDDNodi()

        self._view.update_page()

    def handleBestProdotti(self, e):
        best5=self._model.getBest5()
        self._view.txt_result.controls.append(ft.Text("I 5 prodotti più venduti sono:"))
        for p,score in best5:
            self._view.txt_result.controls.append(ft.Text(f"{p.product_name} with score {score}"))
        self._view.update_page()



    def handleCercaCammino(self, e):
        if len(self._model._graph.nodes) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Errore: Devi prima creare il grafo premendo il pulsante 'Crea grafo'!", color="red")
            )
            self._view.update_page()
            return

        # Controllo che sia stato scelto un nodo dal menu a tendina
        nodo_partenza = self._view._ddProdStart.value
        nodo_arrivo= self._view._ddProdEnd.value
        lunghezza_str=self._view._txtInLun.value


        if nodo_partenza is None or nodo_arrivo is None or lunghezza_str == "":
            self._view.txt_result.controls.append(
                ft.Text("Errore: Seleziona un nodo dal menu a tendina 'Node'! e indicare una lunghezza", color="red")
            )
            self._view.update_page()
            return
        try:
            l_int = int(lunghezza_str)
        except ValueError:
            self._view.txt_result.controls.append("Inserire un valore di lunghezza intero")
            self._view.update_page()
            return
        percorso, peso_massimo = self._model.camminoPiuLungo(l_int,nodo_partenza,nodo_arrivo)
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza : {nodo_partenza}"))

        if len(percorso) <= 1:
            self._view.txt_result.controls.append(ft.Text("Nessun percorso valido trovato con questi vincoli."))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Percorso ottimo trovato; score: {peso_massimo}"))

            # Stampa i nodi del cammino incolonnati riga per riga come richiesto dal layout visivo
            for p in percorso:
                self._view.txt_result.controls.append(ft.Text(f"{(p.product_id)}"))
        self._view.update_page()

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
