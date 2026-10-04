from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        new_nodes.extend(_split_text_node(old_node, delimiter, text_type))
    return new_nodes


def _split_text_node(
    node: TextNode, delimiter: str, text_type: TextType
) -> list[TextNode]:
    # Splitting on the delimiter alternates plain and delimited segments,
    # so a valid string always yields an odd number of parts.
    parts = node.text.split(delimiter)
    if len(parts) % 2 == 0:
        raise ValueError(
            f"Invalid Markdown: unmatched delimiter {delimiter!r} in {node.text!r}"
        )
    split_nodes = []
    for index, part in enumerate(parts):
        if part == "":
            continue
        part_type = text_type if index % 2 == 1 else TextType.TEXT
        split_nodes.append(TextNode(part, part_type))
    return split_nodes
