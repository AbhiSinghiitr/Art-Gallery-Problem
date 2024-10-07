# main.py

from polygon_generator import generate_random_points, create_dcel
from visualiser import visualize_dcel
from monotone import SweepLineAlgorithm

def main(n):
    # Generate random points
    points = generate_random_points(n)
    
    # Create the DCEL
    dcel = create_dcel(points)
    
    # Visualize the original DCEL
    print("Visualizing Original DCEL:")
    visualize_dcel(dcel)
    
    # Step 2: Perform trapezoidalization
    monotone = SweepLineAlgorithm(dcel)
    monotone.process()  # Update method name here
    monotone_dcel,diagonals= monotone.get_dcel()

    # Step 3: Visualize the monotone polygons DCEL
    print("Visualizing Monotone DCEL:")
    visualize_dcel(monotone_dcel,diagonals)

if __name__ == "__main__":
    n = int(input("Enter the number of vertices (e.g., 20): "))
    main(n)
