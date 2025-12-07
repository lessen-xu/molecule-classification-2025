import os
import xml.etree.ElementTree as ET
from src.graph_utils import MoleculeGraph

def parse_gxl(file_path):
    """
    Parses a single .gxl file and returns a MoleculeGraph object.

    Args:
        file_path (str): Path to the .gxl file.

    Returns:
        MoleculeGraph: The populated graph.
    """
    # 1. Parse XML using ElementTree
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find the graph element
    graph_elem = root.find('.//graph')

    if graph_elem is None:
        raise ValueError(f"No graph element found in {file_path}")

    # Extract graph ID
    graph_id = graph_elem.get('id', Path(file_path).stem)

    # 2. Extract nodes and 'symbol' attributes [cite: 399-406]
    nodes = []
    for node_elem in graph_elem.findall('.//node'):
        node_id = node_elem.get('id')

        if node_id is None:
            continue

        # Find the symbol attribute
        symbol_elem = node_elem.find(".//attr[@name='symbol']/string")

        if symbol_elem is not None and symbol_elem.text:
            symbol = symbol_elem.text.strip()
        else:
            symbol = 'X'  # Default

        nodes.append({
            'id': node_id,
            'symbol': symbol
        })

    # 3. Extract edges (undirected) [cite: 410]
    edges = []
    for edge_elem in graph_elem.findall('.//edge'):
        from_node = edge_elem.get('from')
        to_node = edge_elem.get('to')

        if from_node and to_node:
            edges.append({
                'from': from_node,
                'to': to_node
            })

    # Return MoleculeGraph with extracted data
    return MoleculeGraph(graph_id, nodes, edges)


def load_dataset(directory):
    """
    Loads all graphs from a directory.

    Args:
        directory (str): Path to directory containing .gxl files.

    Returns:
        list: List of MoleculeGraph objects.
    """
    graphs = []

    # Handle directory path
    dir_path = Path(directory)

    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Find .gxl files
    gxl_files = list(dir_path.glob('*.gxl'))

    # Check subdirectory if needed
    if not gxl_files:
        gxl_subdir = dir_path / 'gxl'
        if gxl_subdir.exists():
            gxl_files = list(gxl_subdir.glob('*.gxl'))

    if not gxl_files:
        raise FileNotFoundError(f"No .gxl files found in {directory}")

    # Parse each file
    print(f"Loading {len(gxl_files)} molecules...")
    for gxl_file in gxl_files:
        try:
            graph = parse_gxl(str(gxl_file))
            graphs.append(graph)
        except Exception as e:
            print(f"Warning: Could not parse {gxl_file.name}: {e}")

    print(f" Loaded {len(graphs)} graphs")
    return graphs


# ============================================================================
# Utility functions
# ============================================================================

def load_labels(labels_file):
    """Load labels from TSV file."""
    labels = {}
    with open(labels_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                mol_id = parts[0].strip()
                label = parts[1].strip().lower()
                if label in ['active', 'inactive']:
                    labels[mol_id] = label
    return labels


def load_dataset_with_labels(gxl_directory, labels_file):
    """Load graphs with their labels."""
    all_graphs = load_dataset(gxl_directory)
    labels_dict = load_labels(labels_file)

    dataset = []
    for graph in all_graphs:
        # Try to match graph with label
        mol_id = Path(graph.graph_id).stem

        if mol_id in labels_dict:
            dataset.append((graph, labels_dict[mol_id]))
        else:
            # Try alternative matching
            for label_id, label in labels_dict.items():
                if label_id in graph.graph_id:
                    dataset.append((graph, label))
                    break

    return dataset
