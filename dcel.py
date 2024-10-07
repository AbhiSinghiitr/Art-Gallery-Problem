# dcel.py

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type="none"
        self.incident_edge = None

class HalfEdge:
    def __init__(self):
        self.origin = None
        self.next = None
        self.prev = None
        self.twin = None
        self.face = None

class Face:
    def __init__(self):
        self.outer_half_edge = None
        self.inner_half_edges = []

class DCEL:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.faces = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, half_edge):
        self.edges.append(half_edge)

    def add_face(self, face):
        self.faces.append(face)
        
    
    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def get_faces(self):
        return self.faces
