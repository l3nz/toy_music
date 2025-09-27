"""Effettua tutte le trasformazioni sui files.

Si aspetta in input tutto il tree dei files.

Ritorna una lista di tuple con le trasformazioni da applicare.

"""
from pathlib import Path
from itertools import groupby
import re


class Rename:
    """Classe creata per racchiudere tutte le funzioni dei pezzi"""

    FILE_PREFIX = r'^(\d{4})-(.+)$'

    # ( ACTION_RENAME, dir, old_name, new_name)
    ACTION_RENAME = "ren"
    # ( ACTION_DELETE, dir, name )
    ACTION_DELETE = "del"

    def __init__(self):
        # una lista di tuple ('path', 'filename')
        self.src = []
        self.mRwr = {}

    def stats(self):
        "Stampa le statistiche"
        non_unq = self.find_non_uniques()
        max_code = self.find_max_used_code()
        return f"Files: {len(self.src)} (non-uniques: {len(non_unq)}) - Max code: '{self.to_num(max_code)}' - Rewrite rules: {len(self.mRwr)}"

    def rewrites(self, mRewrites):
        "Inserisce regole di riscrittura"
        self.mRwr = mRewrites

    def files_of(self, src):
        "Legge i files ricorsivamente da una directory"
        self.src = [(str(f.parent), f.name)
                    for f in Path(src).rglob('*') if f.is_file()]

    def list_of_filenames(self, lFiles):
        "Per test, carica i files da un array di nomi files"
        def split_fname(filename):
            f = Path(filename)
            return (str(f.parent), f.name)

        self.src = list(map(split_fname, lFiles))

    def keep_good_files(self):
        """
        Tiene solo i file che mi interessamno.
        Li mette tutti in ordine.
        """
        def is_good(ft):
            (_d, filename) = ft
            return filename.endswith(".mp3") and (not filename.startswith("._"))

        good_files = filter(is_good, self.src)
        sorted_files = sorted(good_files)
        self.src = list(sorted_files)

    def find_non_uniques(self):
        """
        Trova tutti i nomi di files che non sono unici.
        Li raggruppa in liste che hanno almeno 2 elementi.
        I gruppi sono formati indipendentemente dalla presenza
        di un prefisso numerico.
        """
        risultato = []
        lista_ordinata = sorted(
            self.src, key=lambda x: self.remove_numeric_prefix(x[1]))
        for _file, gruppo in groupby(lista_ordinata, key=lambda x: self.remove_numeric_prefix(x[1])):
            lista_gruppo = list(gruppo)

            # Aggiungi il gruppo al risultato se contiene più di un elemento.
            if len(lista_gruppo) > 1:
                risultato.append(lista_gruppo)

        return risultato

    def find_max_used_code(self):
        "Trova il codice più elevato già in uso."
        maxCode = 0
        for (_d, f) in self.src:
            v = self.get_numeric_prefix(f)
            if v > maxCode:
                maxCode = v
        return maxCode

    def process_files(self):
        "Crea una lista di comandi per le trasformazioni richieste"
        n = self.find_max_used_code() + 1
        results = []
        for (d, f) in self.src:
            if self.get_numeric_prefix(f) < 0:
                results.append(
                    (self.ACTION_RENAME, d, f, f"{self.to_num(n)}-{f}"))
                n = n + 1
        return results

    @staticmethod
    def get_numeric_prefix(text: str) -> int:
        "Ottiene il prefisso numerico, o -1 se non presente"
        match = re.match(Rename.FILE_PREFIX, text)

        if match:
            return int(match.group(1))
        else:
            return -1

    @staticmethod
    def remove_numeric_prefix(text: str) -> str:
        "Elimina il prefisso (se presente) dal nome del file"
        match = re.match(Rename.FILE_PREFIX, text)

        if match:
            return match.group(2)  # Restituisce tutto dopo il prefisso
        else:
            return text  # Restituisce la stringa originale

    @staticmethod
    def to_num(n: int) -> str:
        """
        Converte un intero (es. 42) in una stringa di 4 caratteri con zeri iniziali (es. '0042').
        """
        if n < 0 or n > 9999:
            raise ValueError(
                "Il numero deve essere compreso tra 0 e 9999 per la formattazione a 4 cifre.")

        return f"{n:04d}"
