class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self._validate(tag, value, children, props)
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def _validate(self, tag, value, children, props):
        if value is not None and children is not None:
            raise ValueError("Tag should contain either value or children, not both")
        if props is not None and not isinstance(props, dict):
            raise ValueError("props must be a dict")
        if children is not None and not isinstance(children, list):
            raise ValueError("children must be a list")
        if tag is not None and not isinstance(tag, str):
            raise ValueError("tag must be a string")

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return ' '.join(map(lambda p: f'{p}="{self.props[p]}"', self.props))

    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
