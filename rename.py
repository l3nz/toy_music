"""Effettua tutte le trasformazioni sui files.

Si aspetta in input tutto il tree dei files.

Ritorna una mappa con le trasformazioni da applicare.

"""
from pathlib import Path
from itertools import groupby

class Rename:
    """Classe creata per racchiudere tutte le funzioni dei pezzi"""

    def __init__(self):
        # una lista di tuple ('path', 'filename')
        self.src = []
        self.mRwr = {}

    def stats(self):
        non_unq = self.find_non_uniques()
        return f"Files: {len(self.src)} (non-uniques: {len(non_unq)}) - Rewrite rules: {len(self.mRwr)}"


    def rewrites(self, mRewrites):
        self.mRwr = mRewrites

    def files_of( self, src ):
        self.src =  [ (str(f.parent), f.name) for f in Path(src).rglob('*') if f.is_file()]

    def list_of_filenames(self, lFiles):
        def split_fname(filename):
            f = Path(filename)
            return (str(f.parent), f.name)

        self.src = list(map( split_fname, lFiles ))

    def find_non_uniques(self):
        risultato = []
        lista_ordinata = sorted(self.src, key=lambda x: x[1])
        for _file, gruppo in groupby(lista_ordinata, key=lambda x: x[1]):
            lista_gruppo = list(gruppo)

            # Aggiungi il gruppo al risultato se contiene più di un elemento.
            if len(lista_gruppo) > 1:
                risultato.append(lista_gruppo)

        return risultato


