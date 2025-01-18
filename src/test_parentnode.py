import unittest
from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
  def tests(self):
    p0 = ParentNode(
          "div",
          [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
          ]
        )
    p1 = ParentNode(
            "p",
            [
              LeafNode("b", "Bold text"),
              LeafNode(None, "Normal text"),
              LeafNode("i", "italic text"),
              LeafNode(None, "Normal text"),
            ],
          )
    p2 = ParentNode(
            "p",
            [
              p0,
              LeafNode("a", "Google", {"href": "https://www.google.com"}),
            ],
          )

    t1 = 'ParentNode(div, None,)\n'
    t1 += ' - LeafNode(b, Bold text,)\n'
    t1 += ' - LeafNode(None, Normal text,)'
    t1h = '<div><b>Bold text</b>Normal text</div>'

    t2 = 'ParentNode(p, None,)\n'
    t2 += ' - LeafNode(b, Bold text,)\n'
    t2 += ' - LeafNode(None, Normal text,)\n'
    t2 += ' - LeafNode(i, italic text,)\n'
    t2 += ' - LeafNode(None, Normal text,)'
    t2h = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'

    t3 = 'ParentNode(p, None,)\n'
    t3 += ' - ParentNode(div, None,)\n'
    t3 += '    - LeafNode(b, Bold text,)\n'
    t3 += '    - LeafNode(None, Normal text,)\n'
    t3 += ' - LeafNode(a, Google, href="https://www.google.com")'
    t3h = '<p><div><b>Bold text</b>Normal text</div><a href="https://www.google.com">Google</a></p>'

    self.assertNotEqual(p0.tag, None)
    self.assertEqual(p0.value, None)
    self.assertNotEqual(p0.children, None)
    self.assertEqual(p0.props, None)

    self.assertEqual(f"{p0}", t1)
    self.assertEqual(f"{p1}", t2)
    self.assertEqual(f"{p2}", t3)

    self.assertEqual(p0.to_html(), t1h)
    self.assertEqual(p1.to_html(), t2h)
    self.assertEqual(p2.to_html(), t3h)

  def test_errors(self):
    pe = ParentNode(None, None)
    pc = ParentNode("p", None)

    with self.assertRaises(ValueError, ) as error:
      pe.to_html()
    self.assertEqual(str(error.exception),"Tag is None. The tag property must be set.")

    with self.assertRaises(ValueError) as error:
      pc.to_html()
    self.assertEqual(str(error.exception),"Children is None. The children property must be set.")

if __name__ == "__main__":
  unittest.main()