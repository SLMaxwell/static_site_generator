from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *

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




def main():
  node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
  
  print()
  print(node)

  node1 = HTMLNode(tag="p", value="Hi There", props= {"href": "https://www.google.com", "target": "_blank",})
  node2 = HTMLNode(tag="p", value="Im P2")
  node3 = HTMLNode(tag='span', value="I'm a span with blue text", props={"class": "blue_text"}, children=[node1, node2])
  node4 = HTMLNode(tag='div', props={"class": "center normal flex_grid"}, children=[node3])

  print()
  print(node1)
  print(node4)

  l1 = LeafNode("p", "This is a paragraph of text.")
  l2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
  l3 = LeafNode(None, "Plain Text")

  print()
  print(l1)
  print(l2)
  print(l3)

  print(l1.to_html())
  print(l2.to_html())
  print(l3.to_html())

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
  print(p0)
  print(p0.to_html())
  print()
  print(p1)
  print(p1.to_html())
  print()
  print(p2)
  print(p2.to_html())


  node = TextNode("This is text with a `code block` word", TextType.TEXT)
  new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
  print(new_nodes)
#   [
#     TextNode("This is text with a ", TextType.TEXT),
#     TextNode("code block", TextType.CODE),
#     TextNode(" word", TextType.TEXT),
# ]

if __name__ == "__main__":
  main()