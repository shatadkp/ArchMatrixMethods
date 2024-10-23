import xml.etree.ElementTree as ET
import csv
import re
from html import unescape

# final code that generates triplets from drawio files

def strip_html_tags(text):
    """Remove HTML tags from a string."""
    if text:
        # Unescape HTML entities
        text = unescape(text)
        # Remove HTML tags
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    return text

def extract_triplets(filename, output_csv):
    # Parse the XML file
    tree = ET.parse(filename)
    root = tree.getroot()

    # Initialize dictionaries to store nodes and edges
    nodes = {}
    edges = []
    node_types = {}

    # Constants for colors
    CLASS_FILL_COLOR = '#f0a30a'
    INDIVIDUAL_FILL_COLOR = '#76608a'
    LITERAL_STROKE_COLOR = 'none'

    # Define the list of predicates that indicate a literal value
    literal_predicates = {
        'has altitude value',
        'has boolean value',
        'has date value',
        'has datetime value',
        'has decimal value',
        'has double value',
        'has integer value',
        'has latitude value',
        'has longitude value',
        'has text value'
    }

    # Find the 'root' element under 'mxGraphModel'
    mxGraphModel = root.find('.//mxGraphModel')
    mxRoot = mxGraphModel.find('root')

    # Build the nodes dictionary and identify node types
    for mxCell in mxRoot.findall('mxCell'):
        cell_id = mxCell.get('id')
        value = mxCell.get('value')
        parent = mxCell.get('parent')
        vertex = mxCell.get('vertex')
        edge = mxCell.get('edge')
        style = mxCell.get('style')

        # Unescape and strip HTML tags from the value
        value = strip_html_tags(value)

        # Check if the cell is a node (vertex)
        if vertex == '1' and edge != '1':
            # Exclude labels attached to edges
            parent_is_edge = any(
                edge_cell.get('id') == parent and edge_cell.get('edge') == '1'
                for edge_cell in mxRoot.findall('mxCell')
            )
            if not parent_is_edge:
                nodes[cell_id] = value

                # Determine node type based on style
                node_type = 'Unknown'
                if style:
                    style_dict = dict(item.split('=') for item in style.split(';') if '=' in item)
                    fillColor = style_dict.get('fillColor', '')
                    strokeColor = style_dict.get('strokeColor', '')

                    if fillColor == CLASS_FILL_COLOR:
                        node_type = 'Class'
                    elif fillColor == INDIVIDUAL_FILL_COLOR:
                        node_type = 'Individual'
                    elif strokeColor == LITERAL_STROKE_COLOR:
                        node_type = 'Literal'

                node_types[cell_id] = node_type

    # Build the edges list
    for mxCell in mxRoot.findall('mxCell'):
        if mxCell.get('edge') == '1':
            source = mxCell.get('source')
            target = mxCell.get('target')
            predicate = mxCell.get('value')

            # Unescape and strip HTML tags from the predicate
            predicate = strip_html_tags(predicate)

            # If the edge has no direct value, check for labels attached to it
            if not predicate:
                predicate = next(
                    (strip_html_tags(child.get('value')) for child in mxRoot.findall('mxCell')
                     if child.get('parent') == mxCell.get('id') and child.get('vertex') == '1'),
                    ''
                )

            edges.append({
                'source': source,
                'target': target,
                'predicate': predicate
            })

    # Create a mapping from node IDs to edges for quick lookup
    source_edges = {}
    for edge in edges:
        source_edges.setdefault(edge['source'], []).append(edge)

    # Ensure 'rdf:type' relations for individuals
    for node_id, node_value in nodes.items():
        if node_types.get(node_id) == 'Individual':
            # Check if there is an 'rdf:type' relation
            has_rdf_type = any(
                edge for edge in source_edges.get(node_id, [])
                if edge['predicate'] == 'rdf:type'
            )
            if not has_rdf_type:
                # Create a blank 'rdf:type' relation
                edges.append({
                    'source': node_id,
                    'predicate': 'rdf:type',
                    'target': ''
                })

    # Ensure 'subclass of' relations for classes
    for node_id, node_value in nodes.items():
        if node_types.get(node_id) == 'Class':
            # Check if there is a 'subclass of' relation
            has_subclass_of = any(
                edge for edge in source_edges.get(node_id, [])
                if edge['predicate'] == 'subclass of'
            )
            if not has_subclass_of:
                # Create a blank 'subclass of' relation
                edges.append({
                    'source': node_id,
                    'predicate': 'subclass of',
                    'target': ''
                })

    # Prepare data for CSV
    individuals_triplets = []
    literals_triplets = []
    rdf_type_triplets = []
    subclass_of_triplets = []

    for edge in edges:
        source_label = nodes.get(edge['source'], edge['source'])
        predicate = edge['predicate']
        target_label = nodes.get(edge['target'], edge['target'])

        source_type = node_types.get(edge['source'], 'Unknown')
        target_type = node_types.get(edge['target'], 'Unknown')

        triplet = [source_label, predicate, target_label]

        if predicate == 'rdf:type':
            rdf_type_triplets.append(triplet)
        elif predicate == 'subclass of':
            subclass_of_triplets.append(triplet)
        elif predicate in literal_predicates:
            literals_triplets.append(triplet)
        elif source_type == 'Individual' and predicate not in ['rdf:type', 'subclass of']:
            individuals_triplets.append(triplet)
        # You can add an else clause to handle other triplets if needed

    # Write to CSV file in the desired order
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Subject', 'Predicate', 'Object'])

        # Write triplets in the specified order
        for triplet in individuals_triplets:
            csvwriter.writerow(triplet)
        for triplet in literals_triplets:
            csvwriter.writerow(triplet)
        for triplet in rdf_type_triplets:
            csvwriter.writerow(triplet)
        for triplet in subclass_of_triplets:
            csvwriter.writerow(triplet)

    print(f"Triplets have been written to {output_csv}")

# Example usage
extract_triplets('UDiagram.drawio', 'output_tripletsU3.csv')
