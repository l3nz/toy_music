"""file creato per unittest"""

import unittest
from rename import Rename



class TestRename(unittest.TestCase):
    """test per il file rename.py"""

    def test_creazione(self):
        """test di funzionamento istanzazione classe"""
        r = Rename()
        self.assertEqual("Files: 0 (non-uniques: 0) - Rewrite rules: 0", r.stats())

    def test_files_of(self):
        """Test di caricamento dei files"""
        r = Rename()
        r.files_of(".")
        # controlla che ci siano questo stessi files
        self.assertIn( ('.', 'rename_unittest.py') , r.src)

    def test_list_of_filenames(self):
        """Test di caricamento dei files"""
        r = Rename()
        r.list_of_filenames([ "a.mp3", "pippo/b.mp3"])
        # controlla che ci siano questo stessi files
        self.assertIn( ('.', 'a.mp3') , r.src)
        self.assertIn( ('pippo', 'b.mp3') , r.src)

    def test_find_non_uniques(self):
        """Test non unici"""
        r = Rename()
        r.list_of_filenames([ "a.mp3", "x/b.mp3", "x/a.mp3", "y/c.mp3", "c.mp3" ])
        unq = r.find_non_uniques()
        self.assertEqual(2, len(unq))
        self.assertIn( [('y', 'c.mp3'), ('.', 'c.mp3')] , unq)
        self.assertIn( [('.', 'a.mp3'), ('x', 'a.mp3')] , unq)
    

    def test_stats(self):
        """Le statistiche"""
        r = Rename()
        r.list_of_filenames([ "a.mp3", "pippo/b.mp3", "pluto/b.mp3"])
        r.rewrites( {"a": "aaaa", "aa": "aaaaaa"})
        
        self.assertEqual("Files: 3 (non-uniques: 1) - Rewrite rules: 2", r.stats())
