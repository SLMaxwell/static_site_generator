from textnode import *
from htmlnode import *
from leafnode import *

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

if __name__ == "__main__":
  main()