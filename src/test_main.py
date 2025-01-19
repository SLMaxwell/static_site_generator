import unittest
from main import *
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
    self.assertEqual(str(error.exception), "Unknown TextType encountered: CRAP")

  def test_split_nodes(self):
    expect = "["
    expect += 'TextNode(This is text with a , TEXT, None), '
    expect += 'TextNode(code block, CODE, None), '
    expect += 'TextNode( word, TEXT, None)'
    expect += ']'

    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(str(new_nodes), expect)

    expect = "["
    expect += 'TextNode(This is text with a , TEXT, None), '
    expect += 'TextNode(italic block, ITALIC, None), '
    expect += 'TextNode( word, TEXT, None)'
    expect += ']'

    node = TextNode("This is text with a *italic block* word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
    self.assertEqual(str(new_nodes), expect)

    expect = "["
    expect += 'TextNode(This is text with a , TEXT, None), '
    expect += 'TextNode(bold block, BOLD, None), '
    expect += 'TextNode( word, TEXT, None)'
    expect += ']'

    node = TextNode("This is text with a **bold block** word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(str(new_nodes), expect)

    expect = "["
    expect += 'TextNode(Italic, ITALIC, None), '
    expect += 'TextNode(Normal Text , TEXT, None), '
    expect += 'TextNode(Bold Text, BOLD, None), '
    expect += 'TextNode( Normal Again, TEXT, None), '
    expect += 'TextNode(Code, CODE, None)'
    expect += ']'

    node = TextNode("Normal Text **Bold Text** Normal Again", TextType.TEXT)
    nodei = TextNode("Italic", TextType.ITALIC)
    nodec = TextNode("Code", TextType.CODE)
    new_nodes = split_nodes_delimiter([nodei, node, nodec], "**", TextType.BOLD)
    self.assertEqual(str(new_nodes), expect)

    t = TextNode("I`m a bad boy!", TextType.TEXT)
    with self.assertRaises(Exception) as error:
      new_nodes = split_nodes_delimiter([t], "`", TextType.CODE)
    # print(str(error.exception))
    self.assertEqual(str(error.exception), "Unmatched delimiters in node: I`m a bad boy!")


if __name__ == "__main__":
  unittest.main()