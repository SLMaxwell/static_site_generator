import unittest
from main import text_node_to_html_node
from textnode import *

class TestMain(unittest.TestCase):
  def test_text_to_html(self):
    t = TextNode("Normal Text", TextType.TEXT)
    h = text_node_to_html_node(t)
    self.assertEqual(h.to_html(), "Normal Text")

    t = TextNode("Bold Text", TextType.BOLD)
    h = text_node_to_html_node(t)
    self.assertEqual(h.to_html(), "<b>Bold Text</b>")

    t = TextNode("Italic Text", TextType.ITALIC)
    h = text_node_to_html_node(t)
    self.assertEqual(h.to_html(), "<i>Italic Text</i>")

    t = TextNode("Code Text", TextType.CODE)
    h = text_node_to_html_node(t)
    self.assertEqual(h.to_html(), "<code>Code Text</code>")

    t = TextNode("Link Tag", TextType.LINK, "https://www.python.org/")
    h = text_node_to_html_node(t)
    self.assertEqual(h.to_html(), '<a href="https://www.python.org/">Link Tag</a>')

    t = TextNode("Image Alt Text", TextType.IMAGE, "https://shorturl.at/lacRo/")
    h = text_node_to_html_node(t)
    self.assertEqual(h.to_html(), '<img src="https://shorturl.at/lacRo/" alt="Image Alt Text"></img>')

    t = TextNode("Bad Text Node!", "CRAP")
    with self.assertRaises(Exception) as error:
      h = text_node_to_html_node(t)
    print(str(error.exception))
    self.assertEqual(str(error.exception), "Unknown TextType encountered: CRAP")

if __name__ == "__main__":
  unittest.main()