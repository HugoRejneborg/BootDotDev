import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_mixed_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_sibling_parent_nodes(self):
        node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode("b", "one")]),
                ParentNode("li", [LeafNode(None, "two")]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<ul><li><b>one</b></li><li>two</li></ul>",
        )

    def test_to_html_deeply_nested(self):
        node = ParentNode(
            "div",
            [ParentNode("section", [ParentNode("p", [LeafNode("i", "deep")])])],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><p><i>deep</i></p></section></div>",
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"class": "container", "id": "main"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><span>child</span></div>',
        )

    def test_to_html_with_props_on_nested_nodes(self):
        node = ParentNode(
            "p",
            [LeafNode("a", "link", {"href": "https://boot.dev"})],
            {"class": "intro"},
        )
        self.assertEqual(
            node.to_html(),
            '<p class="intro"><a href="https://boot.dev">link</a></p>',
        )

    def test_to_html_empty_children_renders_empty_tag(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_missing_tag_and_children_errors_have_different_messages(self):
        with self.assertRaises(ValueError) as no_tag:
            ParentNode(None, []).to_html()
        with self.assertRaises(ValueError) as no_children:
            ParentNode("div", None).to_html()
        self.assertNotEqual(str(no_tag.exception), str(no_children.exception))

    def test_to_html_child_error_propagates(self):
        node = ParentNode("div", [LeafNode("p", None)])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_nested_parent_without_tag_raises(self):
        node = ParentNode("div", [ParentNode(None, [LeafNode("b", "x")])])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_has_no_value(self):
        node = ParentNode("div", [LeafNode("span", "child")])
        self.assertIsNone(node.value)

    def test_parent_is_htmlnode(self):
        node = ParentNode("div", [])
        self.assertIsInstance(node, HTMLNode)

    def test_parent_repr(self):
        node = ParentNode("div", [LeafNode("b", "hi")], {"class": "x"})
        self.assertEqual(
            repr(node),
            "ParentNode('div', [LeafNode('b', 'hi', None)], {'class': 'x'})",
        )


if __name__ == "__main__":
    unittest.main()
