import unittest
from textnode import TextNode, TextType


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
        node = TextNode("This is a text node", TextType.PLAIN)
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


if __name__ == "__main__":
    unittest.main()
