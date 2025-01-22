from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *
import re

def block_to_block_type(block_text):
  if block_text[:7] == "###### ":
    return "h6"
  if block_text[:6] == "##### ":
    return "h5"
  if block_text[:5] == "#### ":
    return "h4"
  if block_text[:4] == "### ":
    return "h3"
  if block_text[:3] == "## ":
    return "h2"
  if block_text[:2] == "# ":
    return "h1"
  if block_text[:3] == "```" and block_text[-3:] == "```":
    return "code"
  
  quote = (block_text[:1] == ">")
  ul = (block_text[:2] in ['* ','- '])
  ol = block_text[:1].isnumeric()

  for i, line in enumerate(block_text.splitlines()):
    # print(line)
    # print(f"{quote}: {line[:1]}")
    if quote and line[:1] != ">":
      quote = False
    if ul and line[:2] not in ['* ','- ']:
      ul = False
    if ol and line[:len(f"{i + 1}. ")] != f"{i + 1}. ":
      ol = False
  
  if quote: return "quote"
  if ul: return "ul"
  if ol: return "ol"
  return "p"

def markdown_to_blocks(markdown):
  blocks = []
  for block in markdown.split("\n\n"):
    cleaned = "\n".join([b.strip() for b in block.strip().splitlines()]).strip()
    if len(cleaned) > 1:
      blocks.append(cleaned)
  return blocks

def text_to_textnodes(text):
  new_nodes = []
  node = TextNode(text, TextType.TEXT)

  new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
  new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
  new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
  new_nodes = split_nodes_image(new_nodes)
  new_nodes = split_nodes_link(new_nodes)

  return new_nodes

def text_node_to_html_node(text_node):
  match text_node.text_type:
    case TextType.TEXT:
      return LeafNode(None, text_node.text)
    case TextType.BOLD:
      return LeafNode("b", text_node.text)
    case TextType.ITALIC:
      return LeafNode("i", text_node.text)
    case TextType.CODE:
      return LeafNode("code", text_node.text)
    case TextType.LINK:
      return LeafNode("a", text_node.text, {"href": text_node.url})
    case TextType.IMAGE:
      return LeafNode("img", '', {"src": text_node.url, "alt": text_node.text})
    case _:
        raise Exception(f"Unknown TextType encountered: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    nodes = []
    outer_type = node.text_type
    if outer_type != TextType.TEXT:
      nodes.append(node)
    else:
      splits = node.text.split(delimiter)
      if len(splits) % 2 == 0:
        raise Exception(f"Unmatched delimiters in node: {node.text[:20]}")
      for i, txt in enumerate(splits):
        type = outer_type if i % 2 == 0 else text_type
        nodes.append(TextNode(txt, type))
    
    new_nodes.extend(nodes)
    
  return new_nodes

def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:
    nodes = []
    outer_type = node.text_type
    if outer_type != TextType.TEXT:
      nodes.append(node)
    else:
      images = extract_markdown_images(node.text)
      names = [i[0] for i in images]
      urls = [i[1] for i in images]
      splits = re.split(r"!\[(.*?)\]\((.*?)\)", node.text)
      for i, txt in enumerate(splits):
        if txt in names:
          nodes.append(TextNode(txt, TextType.IMAGE, urls[names.index(txt)]))
        elif len(txt) > 0 and txt not in urls:
          nodes.append(TextNode(txt, TextType.TEXT))
    
    new_nodes.extend(nodes)
    
  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    nodes = []
    outer_type = node.text_type
    if outer_type != TextType.TEXT:
      nodes.append(node)
    else:
      links = extract_markdown_links(node.text)
      names = [i[0] for i in links]
      urls = [i[1] for i in links]
      splits = re.split(r"[^!]\[(.*?)\]\((.*?)\)", node.text)
      for i, txt in enumerate(splits):
        if txt in names:
          nodes.append(TextNode(txt, TextType.LINK, urls[names.index(txt)]))
        elif len(txt) > 0 and txt not in urls:
          nodes.append(TextNode(txt, TextType.TEXT))
    
    new_nodes.extend(nodes)
    
  return new_nodes

def extract_markdown_images(text):
  return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
  return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)

def sample_text_node():
  node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
  
  print()
  print("Text Node Sample:")
  print(node)

def sample_html_node():
  node1 = HTMLNode(tag="p", value="Hi There", props= {"href": "https://www.google.com", "target": "_blank",})
  node2 = HTMLNode(tag="p", value="Im P2")
  node3 = HTMLNode(tag='span', value="I'm a span with blue text", props={"class": "blue_text"}, children=[node1, node2])
  node4 = HTMLNode(tag='div', props={"class": "center normal flex_grid"}, children=[node3])

  print()
  print("HTML Node Tests:")
  print(node1)
  print(node4)

def sample_leaf_node():
  l1 = LeafNode("p", "This is a paragraph of text.")
  l2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
  l3 = LeafNode(None, "Plain Text")

  print()
  print("Leaf Node Tests:")
  print(l1)
  print(l2)
  print(l3)

  print(l1.to_html())
  print(l2.to_html())
  print(l3.to_html())

def sample_parent_node():
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
  print()
  print("Parent Node Tests:")
  print(p0)
  print(p0.to_html())
  print()
  print(p1)
  print(p1.to_html())
  print()
  print(p2)
  print(p2.to_html())

def sample_text_node_split():
  node = TextNode("This is text with a `code block` word", TextType.TEXT)
  new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
  print()
  print("Text Node Split:")
  print(new_nodes)
    #   [
    #    TextNode("This is text with a ", TextType.TEXT),
    #    TextNode("code block", TextType.CODE),
    #    TextNode(" word", TextType.TEXT),
    #   ]

def sample_image_extraction():
  text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
  print()
  print("Image Markdown Extraction:")
  print(extract_markdown_images(text))
  # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

def sample_links_extraction():
  text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
  print()
  print("Links Markdown Extraction:")
  print(extract_markdown_links(text))
  # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

def sample_image_text_node():
  text = "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
  text += "and This is text with a link [to boot dev](https://www.boot.dev) "
  text += "yet another image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) "
  text += "and another link [to youtube](https://www.youtube.com/@bootdotdev)"

  node = TextNode(text, TextType.TEXT)
  sample = split_nodes_image([node])
  sample = split_nodes_link(sample)

  print()
  print("Split Node Image and Link:")
  print(str(sample))
  # [
  #  TextNode(This is text with an image , TEXT, None),
  #  TextNode(rick roll, IMAGE, https://i.imgur.com/aKaOqIh.gif),
  #  TextNode( and This is text with a link, TEXT, None),
  #  TextNode(to boot dev, LINK, https://www.boot.dev),
  #  TextNode( yet another image , TEXT, None),
  #  TextNode(obi wan, IMAGE, https://i.imgur.com/fJRm4Vk.jpeg),
  #  TextNode( and another link, TEXT, None),
  #  TextNode(to youtube, LINK, https://www.youtube.com/@bootdotdev)
  #]



  #[
  # TextNode(This is text with an image ![rick roll, LINK, https://i.imgur.com/aKaOqIh.gif) and This is text with a link), TextNode(to boot dev, LINK, https://www.boot.dev), TextNode( yet another image ![obi wan, LINK, https://i.imgur.com/fJRm4Vk.jpeg) and another link), TextNode(to youtube, LINK, https://www.youtube.com/@bootdotdev), TextNode(, TEXT, None)]

  # [
  #     TextNode("This is text with a link ", TextType.TEXT),
  #     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
  #     TextNode(" and ", TextType.TEXT),
  #     TextNode(
  #         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
  #     ),
  # ]

def sample_full_text_split():
  text = 'This is **text** with an *italic* word and a `code block` '
  text += 'and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'

  new_nodes = text_to_textnodes(text)
  
  print()
  print("Full Text Split:")
  print(new_nodes)

def sample_block_split():
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
  blocks = markdown_to_blocks(text)

  print()
  print("Splits Blocks:")
  for i, block in enumerate(blocks):
    print(f"Block {i}:")
    print(block)
    print()

def sample_block_types():
  text = "#### This is a heading \n"
  text += "\n"
  text += "\n"
  text += "   This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
  text += "\n"
  text += "\n"
  text += "\n"
  text += "     * This is the first list item in a list block    \n"
  text += "    - This is a list item   \n"
  text += "* This is another list item\n"
  text += "\n"
  text += "```Fake code actually a paragraph\n"
  text += "\n"
  text += "```Actual Code block```\n"
  text += "\n"
  text += "# Heading1\n"
  text += "\n"
  text += "     1. line 1    \n"
  text += "    2. line 2   \n"
  text += "3. line 3\n"
  text += "\n"
  text += " > Fake Quote line 1    \n"
  text += "   Fake Quote line 2   \n"
  text += "> Fake Quote line 3\n"
  text += "\n"
  text += " > Quote line 1    \n"
  text += "  > Quote line 2   \n"
  text += "> Quote line 3\n"

  blocks = markdown_to_blocks(text)
  for i, block in enumerate(blocks):
    bt = block_to_block_type(block)
    print(f"Block {i}: ({bt})")
    print(block)

def main():
  
  sample_text_node()
  sample_html_node()
  sample_leaf_node()
  sample_parent_node()
  sample_text_node_split()
  sample_image_extraction()
  sample_links_extraction()
  sample_image_text_node()
  sample_full_text_split()
  sample_block_split()
  sample_block_types()


if __name__ == "__main__":
  main()