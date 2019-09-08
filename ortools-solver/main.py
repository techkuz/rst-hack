import argparse
import json
import numpy as np

from clustering import recursive_dbscan
from preprocess import preprocess_data
from ORToolsSolver import get_solution

parser = argparse.ArgumentParser(description='Dostavista solver')
parser.add_argument('--input', '-i',
                    help='an integer for the accumulator')
parser.add_argument('--output', '-o',
                    help='sum the integers (default: find the max)')

args = parser.parse_args()

if __name__ == '__main__':
    
    data = json.load(open(args.input))
    couriers = data['couriers']
    depots = data['depots']
    orders = data['orders']
    
    # depots are ignored for now
    depots = []
    
    couriers, orders = preprocess_data(couriers, orders)
    
    X = np.array([[order['pickup_location_x'], order['pickup_location_y']] for order in orders])
    
    clusters = recursive_dbscan(X, np.arange(len(X)))
    
    solution = get_solution(couriers, orders, depots, clusters)
    
    json.dump(solution, open(args.output, 'w'))