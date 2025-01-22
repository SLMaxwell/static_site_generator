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

  def test_extractions(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
    text += "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    ai = "["
    ai += "('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), "
    ai += "('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')"
    ai += "]"

    images = extract_markdown_images(text)
    self.assertEqual(str(images), ai)

    text = "This is text with a link [to boot dev](https://www.boot.dev) "
    text += "and [to youtube](https://www.youtube.com/@bootdotdev)"
    al = "["
    al += "('to boot dev', 'https://www.boot.dev'), "
    al += "('to youtube', 'https://www.youtube.com/@bootdotdev')"
    al += "]"

    links = extract_markdown_links(text)
    self.assertEqual(str(links), al)

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
    text += "and This is text with a link [to boot dev](https://www.boot.dev) "
    text += "yet another image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) "
    text += "and another link [to youtube](https://www.youtube.com/@bootdotdev)"

    ab = "["
    ab += "('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), "
    ab += "('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg'), "
    ab += "('to boot dev', 'https://www.boot.dev'), "
    ab += "('to youtube', 'https://www.youtube.com/@bootdotdev')"
    ab += "]"

    check = extract_markdown_images(text)
    check.extend(extract_markdown_links(text))
    self.assertEqual(str(check), ab)

    nothing = extract_markdown_images("No images")
    self.assertEqual(str(nothing), "[]")
    nothing = extract_markdown_links("No Links")
    self.assertEqual(str(nothing), "[]")
    nothing = extract_markdown_images("")
    self.assertEqual(str(nothing), "[]")
    nothing = extract_markdown_links("")
    self.assertEqual(str(nothing), "[]")

  def test_image_link_split(self):
    text = "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
    text += "and This is text with a link [to boot dev](https://www.boot.dev) "
    text += "yet another image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) "
    text += "and another link [to youtube](https://www.youtube.com/@bootdotdev)"

    a = '['
    a += 'TextNode(This is text with an image , TEXT, None), '
    a += 'TextNode(rick roll, IMAGE, https://i.imgur.com/aKaOqIh.gif), '
    a += 'TextNode( and This is text with a link, TEXT, None), '
    a += 'TextNode(to boot dev, LINK, https://www.boot.dev), '
    a += 'TextNode( yet another image , TEXT, None), '
    a += 'TextNode(obi wan, IMAGE, https://i.imgur.com/fJRm4Vk.jpeg), '
    a += 'TextNode( and another link, TEXT, None), '
    a += 'TextNode(to youtube, LINK, https://www.youtube.com/@bootdotdev)'
    a += ']'

    node = TextNode(text, TextType.TEXT)
    sample = split_nodes_image([node])
    sample = split_nodes_link(sample)

    self.assertEqual(str(sample), a)

    node = TextNode("Hi there", TextType.TEXT)
    sample = split_nodes_image([node])
    sample = split_nodes_link(sample)

    self.assertEqual(str(sample), "[TextNode(Hi there, TEXT, None)]")

    node = TextNode("", TextType.TEXT)
    sample = split_nodes_image([node])
    sample = split_nodes_link(sample)

    self.assertEqual(str(sample), "[]")

    sample = split_nodes_image([])
    sample = split_nodes_link(sample)

    self.assertEqual(str(sample), "[]")

  def test_full_text_split(self):
    text = 'This is **text** with an *italic* word and a `code block` '
    text += 'and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'

    a = '['
    a += 'TextNode(This is , TEXT, None), '
    a += 'TextNode(text, BOLD, None), '
    a += 'TextNode( with an , TEXT, None), '
    a += 'TextNode(italic, ITALIC, None), '
    a += 'TextNode( word and a , TEXT, None), '
    a += 'TextNode(code block, CODE, None), '
    a += 'TextNode( and an , TEXT, None), '
    a += 'TextNode(obi wan image, IMAGE, https://i.imgur.com/fJRm4Vk.jpeg), '
    a += 'TextNode( and a, TEXT, None), '
    a += 'TextNode(link, LINK, https://boot.dev)'
    a += ']'

    new_nodes = text_to_textnodes(text)
    self.assertEqual(str(new_nodes), a)

    new_nodes = text_to_textnodes("Some simple **bold** text.")
    a  = '['
    a += 'TextNode(Some simple , TEXT, None), '
    a += 'TextNode(bold, BOLD, None), '
    a += 'TextNode( text., TEXT, None)'
    a += ']'
    self.assertEqual(str(new_nodes), a)

    new_nodes = text_to_textnodes("Hi There")
    self.assertEqual(str(new_nodes), "[TextNode(Hi There, TEXT, None)]")

    new_nodes = text_to_textnodes("")
    self.assertEqual(str(new_nodes), "[]")

    with self.assertRaises(Exception) as error:
      new_nodes = text_to_textnodes("Bad `code.")
    self.assertEqual(str(error.exception), "Unmatched delimiters in node: Bad `code.")

  def test_block_split(self):
    text = "# This is a heading \n"
    text += "\n"
    text += "\n"
    text += "   This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
    text += "\n"
    text += "\n"
    text += "\n"
    text += "     * This is the first list item in a list block    \n"
    text += "    * This is a list item   \n"
    text += "* This is another list item"

    a0 = "# This is a heading"
    a1 = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
    a2  = "* This is the first list item in a list block\n"
    a2 += "* This is a list item\n"
    a2 += "* This is another list item"

    blocks = markdown_to_blocks(text)

    self.assertEqual(blocks[0], a0)
    self.assertEqual(blocks[1], a1)
    self.assertEqual(blocks[2], a2)

    blocks = markdown_to_blocks(" \n \n\n \n \n\n\n     \n\n     \n     ")
    self.assertEqual(blocks, [])

  def test_block_type(self):
    
    bt = block_to_block_type("# Header")
    self.assertEqual(bt, "h1")
    bt = block_to_block_type("## Header")
    self.assertEqual(bt, "h2")
    bt = block_to_block_type("### Header")
    self.assertEqual(bt, "h3")
    bt = block_to_block_type("#### Header")
    self.assertEqual(bt, "h4")
    bt = block_to_block_type("##### Header")
    self.assertEqual(bt, "h5")
    bt = block_to_block_type("###### Header")
    self.assertEqual(bt, "h6")

    bt = block_to_block_type("```Fake Code")
    self.assertNotEqual(bt, "code")
    self.assertEqual(bt, "p")
    bt = block_to_block_type("Fake Code```")
    self.assertNotEqual(bt, "code")
    self.assertEqual(bt, "p")
    bt = block_to_block_type("```Actual Code```")
    self.assertEqual(bt, "code")
    self.assertNotEqual(bt, "p")

    t  = "> Fake quote\n"
    t += "Fake quote\n"
    t += "> Fake quote"
    bt = block_to_block_type(t)
    self.assertNotEqual(bt, "quote")
    self.assertEqual(bt, "p")

    t  = "> real quote\n"
    t += "> real quote\n"
    t += "> real quote"
    bt = block_to_block_type(t)
    self.assertEqual(bt, "quote")
    self.assertNotEqual(bt, "p")

    t  = "* Fake ul\n"
    t += "- Fake ul\n"
    t += " Fake ul"
    bt = block_to_block_type(t)
    self.assertNotEqual(bt, "ul")
    self.assertEqual(bt, "p")

    t  = "* real quote\n"
    t += "- real quote\n"
    t += "* real quote"
    bt = block_to_block_type(t)
    self.assertEqual(bt, "ul")
    self.assertNotEqual(bt, "p")

    t  = "1. Fake ol\n"
    t += "7 Fake ol\n"
    t += " Fake 0l"
    bt = block_to_block_type(t)
    self.assertNotEqual(bt, "ol")
    self.assertEqual(bt, "p")

    t  = "1. real ol\n"
    t += "2. real ol\n"
    t += "3. real ol"
    bt = block_to_block_type(t)
    self.assertEqual(bt, "ol")
    self.assertNotEqual(bt, "p")

if __name__ == "__main__":
  unittest.main()