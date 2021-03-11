import unittest

# Run tests without using GPU
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import sys
from pathlib import Path
TEST_DIR = str(Path(__file__).parent.resolve())
BASE_DIR = str(Path(__file__).parent.parent.resolve())
sys.path.append(BASE_DIR)

from core.snippet import SnippetExtractor, CombinationalMapping
from core.documents import Document, Patent

class TestSnippetExtractor(unittest.TestCase):

	def setUp(self):
		self.query = 'fluid formation sampling'
		self.longquery = 'A method of sampling formation fluids. The method includes lowering a sampling apparatus into a borewell.'
		self.doc = Document('US7654321B2')
		self.text = self.doc.full_text

	def test_can_create_snippet(self):
		snip = SnippetExtractor.extract_snippet(self.query, self.text)
		self.assertIsInstance(snip, str)
		self.assertGreater(len(snip), 10)

	def test_can_do_mapping(self):
		mapping = SnippetExtractor.map(self.longquery, self.text)
		self.assertIsInstance(mapping, list)
		self.assertGreater(len(mapping), 1)


class CombinationalMappingClass(unittest.TestCase):

	def setUp(self):
		self.el1 = 'A fire fighting drone for fighting forest fires.'
		self.el2 =  'The done uses dry ice to extinguish the fire.'
		self.query = self.el1 + ' ' + self.el2
		self.text1 = Patent('US20010025712A1').full_text # drone patent
		self.text2 = Patent('US20170087393A1').full_text # dry ice patent

	def test_mapping_operation(self):
		texts = [self.text1, self.text2]
		mapping = CombinationalMapping(self.query, texts).map()
		self.assertIsInstance(mapping, list)
		self.assertEqual(2, len(mapping))
		self.assertTrue(all([isinstance(m, dict) for m in mapping]))
		self.assertNotEqual(mapping[0]['doc'], mapping[1]['doc'])

	def test_can_create_mappiing_table(self):
		texts = [self.text1, self.text2]
		table = CombinationalMapping(self.query, texts).map(table=True)
		
		self.assertEqual(len(table), 3) # 2 element rows, 1 header row

		# assert first column
		self.assertEqual(self.el1, table[1][0])
		self.assertEqual(self.el2, table[2][0])

		self.assertEqual('', table[1][2]) # 1st element mapped to first text
		self.assertEqual('', table[2][1]) # 2nd element mapped to second text

if __name__ == '__main__':
	unittest.main()