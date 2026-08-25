import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Google",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_single_prop(self):
        node = HTMLNode("a", "Boot.dev", None, {"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Just some text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "Just some text", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_defaults_are_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_children_are_stored(self):
        child = HTMLNode("span", "child text")
        parent = HTMLNode("div", None, [child])
        self.assertEqual(parent.children, [child])

    def test_to_html_raises(self):
        node = HTMLNode("p", "Just some text")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("a", "Boot.dev", None, {"href": "https://boot.dev"})
        self.assertEqual(
            repr(node),
            "HTMLNode('a', 'Boot.dev', None, {'href': 'https://boot.dev'})",
        )


if __name__ == "__main__":
    unittest.main()
