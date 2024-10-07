import matplotlib.pyplot as plt

def visualize_dcel(dcel, diagonals=None):
    plt.figure()
    
    # Draw vertices
    for vertex in dcel.vertices:
        plt.plot(vertex.x, vertex.y, 'o', color='red')

    # Draw edges (in blue)
    for edge in dcel.edges:
        if edge.origin:
            next_edge = edge.next
            if next_edge:  # Check if next_edge is not None
                plt.plot([edge.origin.x, next_edge.origin.x],
                         [edge.origin.y, next_edge.origin.y], color='blue')
    
    # Draw diagonals (in green)
    if diagonals:
        for diagonal in diagonals:
            v1, v2 = diagonal
            plt.plot([v1.x, v2.x], [v1.y, v2.y], color='green', linestyle='--')

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('DCEL Visualization with Diagonals')
    plt.grid()
    plt.axis('equal')
    plt.show()
