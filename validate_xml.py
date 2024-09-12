import xml.etree.ElementTree as ET
from xml.etree.ElementTree import SubElement


def validate_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    if root.find('id') is None:
        raise ValueError("Id tag but not present in {}".format(xml_file))
    if root.find('name') is None:
        raise ValueError("Name tag but not present in {}".format(xml_file))

    graph = {'id': root.find('id').text, 'graph_name': root.find('name').text}
    graph_id = graph.get('id')

    node_ids = []
    for node in root.find('nodes'):
        node_ids.append(node.find('id').text)

    if len(node_ids) < 1:
        raise ValueError("Expected 1 or more nodes")

    if len(node_ids) != len(set(node_ids)):
        raise ValueError("Node ids are not unique")

    edges = []

    for node in root.find('edges'):
        if len(node.findall('from')) > 1:
            raise ValueError("Cannot have more than one from tag in an edge node")
        if len(node.findall('to')) > 1:
            raise ValueError("Cannot have more than one to tag in an edge node")
        if node.find('from').text not in node_ids:
            raise ValueError('from node id does not exist under nodes')
        if node.find('to').text not in node_ids:
            raise ValueError('to node id does not exist under nodes')
        if node.find('cost') is None:
            SubElement(node, 'cost').text = '0'
        edges.append({'edge_to': node.find('to').text,
                      'edge_from': node.find('from').text,
                      'cost': float(node.find('cost').text),
                      'id': node.find('id').text,
                      'graph_id': graph_id})
    return graph, edges





