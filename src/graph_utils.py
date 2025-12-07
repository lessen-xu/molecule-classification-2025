class MoleculeGraph:
    """
    Standard representation of a molecule for the team.
    """
    def __init__(self, id):
        self.id = id
        self.nodes = {}  # {node_id: label} e.g. {'_1': 'C'}
        self.edges = []  # List of tuples [('_1', '_2'), ...]
        
    def add_node(self, node_id, label):
        self.nodes[node_id] = label
        
    def add_edge(self, source, target):
        # Undirected graph: treat (u, v) same as (v, u)
        self.edges.append((source, target))

    def __repr__(self):
        return f"Graph({self.id}, {len(self.nodes)} nodes, {len(self.edges)} edges)"