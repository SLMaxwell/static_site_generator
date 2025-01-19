import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    node3 = TextNode("This is a simple node", TextType.BOLD)
    node4 = TextNode("This is a text node", TextType.ITALIC)
    node5 = TextNode("Link to Google", TextType.LINK, "https://www.google.com/")
    node6 = TextNode("Link to Google", TextType.LINK, "https://www.google.com/")
    node7 = TextNode("Link to Google", TextType.LINK, "https://www.boot.dev/")

    text  = f"{node}"
    text2 = f"{node2}"
    text3 = f"{node3}"
    text4 = f"{node4}"
    text5 = f"{node5}"
    text6 = f"{node6}"
    text7 = f"{node7}"
    
    self.assertEqual(node, node2)
    self.assertNotEqual(node, node3)
    self.assertNotEqual(node, node4)

    self.assertEqual(node5, node6)
    self.assertNotEqual(node5, node7)
    
    self.assertEqual(text, text2)
    self.assertNotEqual(text, text3)
    self.assertNotEqual(text, text4)

    self.assertEqual(text5, text6)
    self.assertNotEqual(text5, text7)


if __name__ == "__main__":
  unittest.main()