import unittest
from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_url_defaults_to_none(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_none_vs_set(self):
        node = TextNode("Boot.dev", TextType.LINK)
        node2 = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_not_eq_other_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, "This is a text node")

    def test_repr(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        self.assertEqual(
            repr(node), "TextNode('Boot.dev', link, 'https://boot.dev')"
        )


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_renders_raw(self):
        node = TextNode("raw text", TextType.TEXT)
        self.assertEqual(text_node_to_html_node(node).to_html(), "raw text")

    def test_bold(self):
        node = TextNode("bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold")
        self.assertEqual(html_node.to_html(), "<b>bold</b>")

    def test_italic(self):
        node = TextNode("italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>italic</i>")

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>print('hi')</code>")

    def test_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})
        self.assertEqual(
            html_node.to_html(), '<a href="https://boot.dev">Boot.dev</a>'
        )

    def test_image(self):
        node = TextNode("A cute cat", TextType.IMAGE, "https://example.com/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/cat.png", "alt": "A cute cat"},
        )

    def test_returns_leaf_node(self):
        for text_type in TextType:
            node = TextNode("x", text_type, "https://boot.dev")
            with self.subTest(text_type=text_type):
                self.assertIsInstance(text_node_to_html_node(node), LeafNode)

    def test_unsupported_type_raises(self):
        node = TextNode("x", "underline")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
