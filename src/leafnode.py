from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)
        pass

    def to_html(self):
        if self.value is None:
            raise ValueError("Value cannot be empty")

        if not self.tag or self.tag.strip() == "":
            return self.value

        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        return f"<{self.tag} {super().props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(value={self.value}, tag={self.tag}, props={self.props})"
