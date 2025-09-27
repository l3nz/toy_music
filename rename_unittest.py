"""file creato per unittest"""

import unittest
from rename import Rename


class TestRename(unittest.TestCase):
    """test per il file rename.py"""

    def test_creazione(self):
        """test di funzionamento istanzazione classe"""
        r = Rename()
        self.assertEqual(
            "Files: 0 (non-uniques: 0) - Max code: '0000' - Rewrite rules: 0", r.stats())

    def test_files_of(self):
        """Test di caricamento dei files"""
        r = Rename()
        r.files_of(".")
        # controlla che ci siano questo stessi files
        self.assertIn(('.', 'rename_unittest.py'), r.src)

    def test_list_of_filenames(self):
        """Test di caricamento dei files"""
        r = Rename()
        r.list_of_filenames(["a.mp3", "pippo/b.mp3"])
        # controlla che ci siano questo stessi files
        self.assertIn(('.', 'a.mp3'), r.src)
        self.assertIn(('pippo', 'b.mp3'), r.src)

    def test_keep_good(self):
        """Test di caricamento dei files"""
        r = Rename()
        r.list_of_filenames(["a.mp3",
                             "._b.mp3",
                             "c.wav",
                             "x/3.mp3",
                             "y/2.mp3",
                             "x/1.mp3",
                             "y/9.mp3"

                             ])
        r.keep_good_files()
        # controlla che ci siano questo stessi files
        self.assertEqual([('.', 'a.mp3'),
                          ('x', '1.mp3'),
                          ('x', '3.mp3'),
                          ('y', '2.mp3'),
                          ('y', '9.mp3')], r.src)

    def test_find_non_uniques(self):
        """Test non unici"""
        r = Rename()
        r.list_of_filenames(
            ["a.mp3", "x/b.mp3", "x/a.mp3", "y/c.mp3", "c.mp3"])
        unq = r.find_non_uniques()
        self.assertEqual(2, len(unq))
        self.assertIn([('y', 'c.mp3'), ('.', 'c.mp3')], unq)
        self.assertIn([('.', 'a.mp3'), ('x', 'a.mp3')], unq)

    def test_find_non_uniques_with_prefix(self):
        """Test non unici con prefisso"""
        r = Rename()
        r.list_of_filenames(
            ["0003-a.mp3", "x/b.mp3", "x/0004-a.mp3", "y/c.mp3", "0002-c.mp3"])
        unq = r.find_non_uniques()
        self.assertEqual(2, len(unq))
        self.assertIn([('y', 'c.mp3'), ('.', '0002-c.mp3')], unq)
        self.assertIn([('.', '0003-a.mp3'), ('x', '0004-a.mp3')], unq)

    def test_find_max_code_none(self):
        """Test non unici"""
        r = Rename()
        r.list_of_filenames(
            ["a.mp3", "x/b.mp3", "x/a.mp3", "y/c.mp3", "c.mp3"])
        self.assertEqual(0, r.find_max_used_code())

    def test_find_max_code_present(self):
        """Test non unici"""
        r = Rename()
        r.list_of_filenames(["0023-a.mp3", "x/0054-b.mp3",
                            "x/0002-a.mp3", "y/c.mp3", "c.mp3"])
        self.assertEqual(54, r.find_max_used_code())

    def test_stats(self):
        """Le statistiche"""
        r = Rename()
        r.list_of_filenames(["a.mp3", "pippo/b.mp3", "pluto/b.mp3"])
        r.rewrites({"a": "aaaa", "aa": "aaaaaa"})

        self.assertEqual(
            "Files: 3 (non-uniques: 1) - Max code: '0000' - Rewrite rules: 2", r.stats())

    def test_process_simple(self):
        r = Rename()
        r.list_of_filenames(["a.mp3", "pippo/b.mp3", "pluto/b.mp3"])
        r.keep_good_files()
        new_files = r.process_files()
        self.assertEquals([('ren', '.', 'a.mp3', '0001-a.mp3'),
                           ('ren', 'pippo', 'b.mp3', '0002-b.mp3'),
                           ('ren', 'pluto', 'b.mp3', '0003-b.mp3')],
                          new_files)

    def test_process_with_existing(self):
        r = Rename()
        r.list_of_filenames(["a.mp3", "pippo/0007-b.mp3", "pluto/b.mp3"])
        r.keep_good_files()
        new_files = r.process_files()
        self.assertEquals([('ren', '.', 'a.mp3', '0008-a.mp3'),
                           ('ren', 'pluto', 'b.mp3', '0009-b.mp3')],
                          new_files)

    def test_process_from_file(self):
        with open('00allfiles.txt', 'r') as f:
            lines = f.read().splitlines()

        r = Rename()
        r.list_of_filenames(lines)
        r.keep_good_files()
        print(f"\n\nSTATS: {r.stats()}")

        new_files = r.process_files()
        for cmd in new_files:
            print(f" - {cmd}")
