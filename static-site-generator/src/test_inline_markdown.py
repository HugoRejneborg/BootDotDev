import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode("An _italic_ word", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC),
            [
                TextNode("An ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_multiple_delimited_sections(self):
        node = TextNode("**one** and **two** and **three**", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("three", TextType.BOLD),
            ],
        )

    def test_delimiter_at_start(self):
        node = TextNode("`code` first", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("code", TextType.CODE),
                TextNode(" first", TextType.TEXT),
            ],
        )

    def test_delimiter_at_end(self):
        node = TextNode("last `code`", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("last ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_whole_text_delimited(self):
        node = TextNode("**all bold**", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [TextNode("all bold", TextType.BOLD)],
        )

    def test_no_delimiter_returns_node_unchanged(self):
        node = TextNode("plain text only", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [TextNode("plain text only", TextType.TEXT)],
        )

    def test_non_text_nodes_pass_through(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC), nodes)

    def test_non_text_node_with_delimiter_is_not_split(self):
        node = TextNode("x `not split` y", TextType.CODE)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [node])

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("a `b` c", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("`d` e", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "`", TextType.CODE),
            [
                TextNode("a ", TextType.TEXT),
                TextNode("b", TextType.CODE),
                TextNode(" c", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("d", TextType.CODE),
                TextNode(" e", TextType.TEXT),
            ],
        )

    def test_chained_calls_handle_bold_then_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(
            nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
        )

    def test_empty_list_returns_empty_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has an `unclosed code block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_unmatched_after_valid_pair_raises(self):
        node = TextNode("**ok** but **broken", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_does_not_mutate_input(self):
        node = TextNode("a `b` c", TextType.TEXT)
        nodes = [node]
        split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(nodes, [TextNode("a `b` c", TextType.TEXT)])


if __name__ == "__main__":
    unittest.main()
