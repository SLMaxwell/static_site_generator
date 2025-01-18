import unittest
from leafnode import LeafNode

class TestHTMLNode(unittest.TestCase):
  def test_eq(self):
    l1 = LeafNode("p", "This is a paragraph of text.")
    l2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    l3 = LeafNode(None, "Plain Text")

    self.assertEqual(l3.tag, None)
    self.assertNotEqual(l3.value, None)
    self.assertEqual(l3.children, None)
    self.assertEqual(l3.props, None)

    self.assertEqual(f"{l1}", "LeafNode(p, This is a paragraph of text.,)")
    self.assertEqual(f"{l2}", 'LeafNode(a, Click me!, href="https://www.google.com")')
    self.assertEqual(f"{l3}", 'LeafNode(None, Plain Text,)')

    self.assertEqual(l1.to_html(), '<p>This is a paragraph of text.</p>')
    self.assertEqual(l2.to_html(), '<a href="https://www.google.com">Click me!</a>')
    self.assertEqual(l3.to_html(), 'Plain Text')

if __name__ == "__main__":
  unittest.main()