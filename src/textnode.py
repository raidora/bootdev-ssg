class TextNode:
    valid_types = ["bold", "italic", "strikethrough", "underline"]

    def __init__(self, text, text_type, url=None):
        if not isinstance(text, str):
            raise TypeError("Text must be of type string")
        if text_type is None or text_type not in self.valid_types:
            raise TypeError("text_type must be one of " + ", ".join(self.valid_types))
        if url is not None and not isinstance(url, str):
            raise TypeError("url must be of type string")

        if url == "":
            self.url = None
        else:
            self.url = url

        self.text = text
        self.text_type = text_type

    def __eq__(self, other):
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
