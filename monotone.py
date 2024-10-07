import heapq
from dcel import Face, HalfEdge, Vertex, DCEL  # Import the necessary classes

class SweepLineAlgorithm:
    def __init__(self, dcel):
        self.dcel = dcel
        self.event_queue = []  # Priority queue for events (vertices)
        self.status = {}  # Status dictionary (stores active edges)
        self.helper = {}  # Helper vertices for each edge
        self.diagonals = []  # List to store the diagonals
        
    def add_event(self, vertex):
        # Add vertex to the event queue with priority based on y-coordinate (inverted for max-priority)
        heapq.heappush(self.event_queue, (-vertex.y, vertex.x, vertex))
        
    def classify_vertex(self, vertex, prev_vertex, next_vertex):
        def is_below(v1, v2):
            return v1.y < v2.y or (v1.y == v2.y and v1.x > v2.x)

        if is_below(prev_vertex, vertex) and is_below(next_vertex, vertex):
            if self.is_vertex_to_left(vertex, prev_vertex, next_vertex):
                return "start"
            return "split"
        elif is_below(vertex, prev_vertex) and is_below(vertex, next_vertex):
            if self.is_vertex_to_left(vertex, prev_vertex, next_vertex):
                return "end"
            return "merge"
        return "regular"

    def is_vertex_to_left(self, vertex, prev_vertex, next_vertex):
        return (next_vertex.x - vertex.x) * (prev_vertex.y - vertex.y) > \
               (prev_vertex.x - vertex.x) * (next_vertex.y - vertex.y)

    def handle_start_vertex(self, vertex):
        incident_edge = vertex.incident_edge
        self.status[incident_edge] = vertex
        self.helper[incident_edge] = vertex

    def handle_end_vertex(self, vertex):
        prev_edge = vertex.incident_edge.prev

        # Check if the previous edge is in the helper dictionary
        if prev_edge in self.helper and self.helper[prev_edge].type == "merge":
            self.add_diagonal(vertex, self.helper[prev_edge])
        
        # Remove the incident edge from the status
        if vertex.incident_edge in self.status:
            del self.status[vertex.incident_edge]

    def handle_split_vertex(self, vertex):
        left_edge = self.find_left_edge(vertex)
        print(f"In split left edge: ({vertex.x}, {vertex.y}),left edge : ({left_edge.origin.x},{left_edge.origin.y})")
        if left_edge is not None and left_edge in self.helper:
            self.add_diagonal(vertex, self.helper[left_edge])
        self.helper[left_edge] = vertex if left_edge is not None else None
        incident_edge = vertex.incident_edge
        self.status[incident_edge] = vertex
        self.helper[incident_edge] = vertex

    def handle_merge_vertex(self, vertex):
        prev_edge = vertex.incident_edge.prev

        # Check if the previous edge is in the helper dictionary
        if prev_edge in self.helper and self.helper[prev_edge].type == "merge":
            self.add_diagonal(vertex, self.helper[prev_edge])
        
        # Remove the previous edge from the status
        if prev_edge in self.status:
            del self.status[prev_edge]
        
        # Find the left edge from the vertex and check if the helper is "merge"
        left_edge = self.find_left_edge(vertex)
        if left_edge is not None and left_edge in self.helper and self.helper[left_edge].type == "merge":
            print(f"In merege Going up: ({vertex.x}, {vertex.y}),left edge : ({left_edge.origin.x},{left_edge.origin.y})")

            self.add_diagonal(vertex, self.helper[left_edge])
        
        # Update the helper for the left edge to the current vertex
        self.helper[left_edge] = vertex if left_edge is not None else None

    def handle_regular_vertex(self, vertex):
        prev_vertex = vertex.incident_edge.prev.origin
        prev_edge = vertex.incident_edge.prev  # Get the previous edge

        if prev_vertex.y > vertex.y:  # Vertex going down
            # Check if the previous edge is in the helper dictionary
            if prev_edge in self.helper and self.helper[prev_edge].type == "merge":
                self.add_diagonal(vertex, self.helper[prev_edge])
            
            # Remove the previous edge from the status
            if prev_edge in self.status:
                del self.status[prev_edge]
            
            incident_edge = vertex.incident_edge
            self.status[incident_edge] = vertex
            self.helper[incident_edge] = vertex  # Initialize the helper for this edge
        else:  # Vertex going up
            left_edge = self.find_left_edge(vertex)
            if left_edge is not None and left_edge in self.helper and self.helper[left_edge].type == "merge":
                print(f"Going up: ({vertex.x}, {vertex.y}),left edge : ({left_edge.origin.x},{left_edge.origin.y})")
                self.add_diagonal(vertex, self.helper[left_edge])
            
            self.helper[left_edge] = vertex if left_edge is not None else None

    def find_left_edge(self, vertex):
        sorted_edges = sorted(self.status.keys(), key=lambda e: e.origin.x)
        edge1 =None
        for edge in sorted_edges:
            if edge.origin.x < vertex.x:
                edge1 = edge
        return edge1
    
    def add_diagonal(self, vertex1, vertex2):
        # Add a diagonal between vertex1 and vertex2
        print(f"Adding diagonal between ({vertex1.x}, {vertex1.y}) and ({vertex2.x}, {vertex2.y})")
        new_half_edge_1 = HalfEdge()
        new_half_edge_2 = HalfEdge()
        
        new_half_edge_1.origin = vertex1
        new_half_edge_2.origin = vertex2
        
        new_half_edge_1.twin = new_half_edge_2
        new_half_edge_2.twin = new_half_edge_1
        
        # Add the diagonal to the DCEL
        self.dcel.add_edge(new_half_edge_1)
        self.dcel.add_edge(new_half_edge_2)
        
        # Store the diagonal for future reference
        self.diagonals.append((vertex1, vertex2))

    def process(self):
        # Process the event queue to split the polygon into monotone pieces
        for vertex in self.dcel.get_vertices():
            self.add_event(vertex)

        while self.event_queue:
            _, _, vertex = heapq.heappop(self.event_queue)  # Get the vertex with highest priority
            prev_vertex = vertex.incident_edge.prev.origin
            next_vertex = vertex.incident_edge.next.origin
            vertex_type = self.classify_vertex(vertex, prev_vertex, next_vertex)
            print(f"Processing Vertex: ({vertex.x}, {vertex.y}), Type: {vertex_type}")
            vertex.type = vertex_type
            
            if vertex_type == "start":
                self.handle_start_vertex(vertex)
            elif vertex_type == "end":
                self.handle_end_vertex(vertex)
            elif vertex_type == "split":
                self.handle_split_vertex(vertex)
            elif vertex_type == "merge":
                self.handle_merge_vertex(vertex)
            elif vertex_type == "regular":
                self.handle_regular_vertex(vertex)

    def get_dcel(self):
        return self.dcel,self.diagonals
