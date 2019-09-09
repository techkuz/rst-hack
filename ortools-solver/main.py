import argparse
import json
import numpy as np

from clustering import recursive_dbscan
from preprocess import preprocess_data
from ORToolsSolver import get_solution
from utils import order_distance

parser = argparse.ArgumentParser(description='Dostavista solver')
parser.add_argument('--input', '-i',
                    help='an integer for the accumulator')
parser.add_argument('--output', '-o',
                    help='sum the integers (default: find the max)')

args = parser.parse_args()

if __name__ == '__main__':
    np.random.seed(1234)
    
    data = json.load(open(args.input))
    couriers = data['couriers']
    depots = data['depots']
    orders = data['orders']
    
    # depots are ignored for now
    depots = []
    
    couriers, orders = preprocess_data(couriers, orders)
    
    X = np.array([[order['pickup_location_x'], order['pickup_location_y']] for order in orders])
    
    clusters = sorted(recursive_dbscan(X, np.arange(len(X))), key=len)[::-1]


    aggregated = True
    
    while aggregated:
        aggregated = False
        aggregate_clusters = [clusters[0]]
        
        for cluster in clusters[1:]:
            if len(cluster) + len(aggregate_clusters[-1]) < 1500:
                aggregate_clusters[-1] = np.concatenate([aggregate_clusters[-1], cluster])
                aggregated = True
            else:
                aggregate_clusters.append(cluster)
                
        clusters = aggregate_clusters
    
    print(f"Cluster sizes: {np.array(sorted([len(c) for c in clusters]))}")

    solution = get_solution(couriers, orders, depots, aggregate_clusters) 

    json.dump(solution, open(args.output, 'w'))