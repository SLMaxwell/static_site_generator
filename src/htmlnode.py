class HTMLNode:

  def __init__(self, tag=None, value=None, children=None, props=None):
    # An HTMLNode without a tag will just render as raw text
    # An HTMLNode without a value will be assumed to have children
    # An HTMLNode without children will be assumed to have a value
    # An HTMLNode without props simply won't have any attributes
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError("to_html() should be implemented by sub-classes.")
  
  def props_to_html(self):
    text = ""
    if self.props:
      for k, v in self.props.items():
        text += f' {k}="{v}"'
    return text

  def __repr__(self):
    children = ""
    if self.children:
      for n in self.children:
        child = f"{n}"
        for i, l in enumerate(child.split("\n")):
          pre = "\n - " if i == 0 else "\n   "
          children += f"{pre}{l}"

    return f"{type(self).__name__}({self.tag}, {self.value},{self.props_to_html()}){children}"