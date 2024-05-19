from src.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if children is None or (isinstance(children, list) and len(children) == 0):
            raise ValueError("(children) must be a list with at least one element")

    def to_html(self):
        if not self.tag or self.tag.strip() == "":
            raise ValueError("(tag) cannot be empty")

        children = ""
        if self.children:
            for child in self.children:
                children += child.to_html()
        if self.props:
            return f"<{self.tag} {super().props_to_html()}>{children}</{self.tag}>"
        else:
            return f"<{self.tag}>{children}</{self.tag}>"
