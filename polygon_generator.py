# polygon_generator.py

import random
from math import atan2
from dcel import Vertex, HalfEdge, Face, DCEL  # Import the DCEL classes

def generate_random_points(n):
    points = set()  # Use a set to avoid duplicates
    while len(points) < n:
        x = random.uniform(0, 1000)  # Change range to 0-1000
        y = random.uniform(0, 1000)  # Change range to 0-1000
        points.add((x, y))  # Add points to the set
        
    points_list = list(points)
    print("Generated Points:")
    for point in points_list:
        print(point)
    return list(points)
    
def calculate_centroid(points):
    """Calculate the centroid of a list of points."""
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    centroid_x = sum(x_coords) / len(points)
    centroid_y = sum(y_coords) / len(points)
    return (centroid_x, centroid_y)



def create_polygon(points):
    # Use the first point as the reference point for angle sorting
    centroid = calculate_centroid(points)

    
    # Sort points based on the angle with the reference point
    sorted_points = sorted(points, key=lambda p: atan2(p[1] - centroid[1], p[0] - centroid[0]))
    
    return sorted_points   # Return the sorted points directly

def create_dcel(points):
    sorted_points = create_polygon(points)
    dcel = DCEL()

    # Create vertices and add to the DCEL
    vertices = [Vertex(x, y) for (x, y) in sorted_points]
    
    for vertex in vertices:
        dcel.add_vertex(vertex)
    
    # Create half-edges, link them, and set incident edges
    edges = []
    num_vertices = len(vertices)
    
    for i in range(num_vertices):
        he = HalfEdge()
        he.origin = vertices[i]  # Set the origin of the half-edge
        vertices[i].incident_edge = he  # Set incident edge for the vertex
        edges.append(he)
        dcel.add_edge(he)
    
    # Link half-edges circularly (prev and next)
    for i in range(num_vertices):
        edges[i].next = edges[(i + 1) % num_vertices]  # Next edge
        edges[i].prev = edges[(i - 1) % num_vertices]  # Previous edge
    
    # Create the outer face
    outer_face = Face()
    outer_face.outer_half_edge = edges[0]  # Assign the outer face's half-edge
    dcel.add_face(outer_face)

    return dcel