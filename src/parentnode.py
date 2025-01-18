from htmlnode import HTMLNode

class ParentNode(HTMLNode):

  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("Tag is None. The tag property must be set.")
    if self.children is None:
      raise ValueError("Children is None. The children property must be set.")
    
    value = ""
    for child in self.children:
      value += child.to_html()

    return f"<{self.tag}{self.props_to_html()}>{value}</{self.tag}>"