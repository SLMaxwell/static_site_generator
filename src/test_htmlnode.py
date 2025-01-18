import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
  def test_eq(self):
    node0 = HTMLNode(tag='div', value="I'm a Div")
    node1 = HTMLNode(tag="p", value="Hi There", props= {"href": "https://www.google.com", "target": "_blank",})
    node2 = HTMLNode(tag="p", value="Im P2")
    node3 = HTMLNode(tag='span', value="I'm a span with blue text", props={"class": "blue_text"}, children=[node1, node2])
    node4 = HTMLNode(tag='div', props={"class": "center normal flex_grid"}, children=[node3])
    node5 = HTMLNode(value="I should be raw text")

    nested_text = 'HTMLNode(div, None, class="center normal flex_grid")\n'
    nested_text += ' - HTMLNode(span, I\'m a span with blue text, class="blue_text")\n'
    nested_text += '    - HTMLNode(p, Hi There, href="https://www.google.com" target="_blank")\n'
    nested_text += '    - HTMLNode(p, Im P2,)'

    self.assertEqual(node0.props_to_html(), "")
    self.assertEqual(f"{node1}", 'HTMLNode(p, Hi There, href="https://www.google.com" target="_blank")')
    self.assertEqual(f"{node4}", nested_text)
    
    self.assertEqual(node5.tag, None)
    self.assertEqual(node4.value, None)
    self.assertEqual(node2.children, None)
    self.assertEqual(node0.props, None)

if __name__ == "__main__":
  unittest.main()