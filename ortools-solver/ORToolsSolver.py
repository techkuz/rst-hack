from collections import defaultdict
import copy
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, cdist
from tqdm import tqdm

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class ORToolsSolver:

    def __init__(self, couriers, orders, depots):
        
        self.couriers = couriers
        self.orders = orders
        self.depots = depots
        
        courier_positions = [[courier['location_x'], courier['location_y']] for courier in couriers]
        pickup_positions = [[order['pickup_location_x'], order['pickup_location_y']] for order in orders]
        dropoff_positions = [[order['dropoff_location_x'], order['dropoff_location_y']] for order in orders]
        depot_positions = [[depot['location_x'], depot['location_y']] for depot in depots]
        
        self.courier_id_to_node = {courier['courier_id']: idx + 1 for idx, courier in enumerate(couriers)}
        self.pickup_id_to_node = {order['pickup_point_id']: idx + 1 + len(couriers) for idx, order in enumerate(orders)}
        self.dropoff_id_to_node = {order['dropoff_point_id']: idx + 1 + len(couriers) + len(orders) 
                                   for idx, order in enumerate(orders)}
        self.depot_id_to_node = {depot['point_id']: idx + 1 + len(couriers) + 2 * len(orders) for idx, depot in enumerate(depots)}

        all_positions = courier_positions + pickup_positions + dropoff_positions + depot_positions

        self.dist_matrix = cdist(all_positions, all_positions, 'cityblock')
        
#         payments = [order['payment'] for order in orders]
#         all_payments = - 0.5 * np.tile([0] * len(courier_positions) + [0] * len(pickup_positions) + 
#                                        [0] * len(depot_positions) + payments, (len(all_positions), 1))
#         payment_shift = all_payments.min()
#         dist_payment_matrix = dist_matrix + all_payments
#         dist_payment_matrix = dist_payment_matrix - payment_shift
#         dist_payment_matrix[np.diag_indices(dist_payment_matrix.shape[0])] = 0
        
        self.dist_matrix = np.pad(self.dist_matrix, ((1, 0), (1, 0)), mode='constant')
#         self.dist_payment_matrix = np.pad(dist_payment_matrix, ((1, 0), (1, 0)), mode='constant')
        
        # Create the routing index manager.
        self.manager = pywrapcp.RoutingIndexManager(len(self.dist_matrix), len(couriers), 
                                                    list(range(1, len(couriers) + 1)), 
                                                    [0] * len(couriers))

        # Create Routing Model.
        self.routing = pywrapcp.RoutingModel(self.manager)
        
        time_transit_callback_index = self.routing.RegisterTransitCallback(self.time_callback)

#         cost_transit_callback_index = self.routing.RegisterTransitCallback(self.time_callback)
        self.routing.SetArcCostEvaluatorOfAllVehicles(time_transit_callback_index)
        
        # Add Distance constraint.
        self.routing.AddDimension(
            time_transit_callback_index,
            18 * 60,  # courier max wait time
            24 * 60,  # courier maximum travel time
            False,
            'Time')

        time_dimension = self.routing.GetDimensionOrDie('Time')
        time_dimension.SetGlobalSpanCostCoefficient(1)

        # cost is 2 times the distance
        cost_dimension = self.routing.GetDimensionOrDie('Time')
        cost_dimension.SetGlobalSpanCostCoefficient(2)
        
        # Add time window constraints for each pickups and dropoffs
        for order in orders:
            pickup_index = self.manager.NodeToIndex(self.order_to_pickup_node(order))
            dropoff_index = self.manager.NodeToIndex(self.order_to_dropoff_node(order))
            time_dimension.CumulVar(pickup_index).SetRange(order['pickup_from'], order['pickup_to'])
            time_dimension.CumulVar(dropoff_index).SetRange(order['dropoff_from'], order['dropoff_to'])

        # Courier time window
        for courier_index, courier in enumerate(self.couriers):
            index = self.routing.Start(courier_index)
            time_dimension.CumulVar(index).SetRange(courier['from'], courier['to'])

        for i in range(len(couriers)):
#             self.routing.AddVariableMinimizedByFinalizer(
#                 cost_dimension.CumulVar(self.routing.Start(i)))
            self.routing.AddVariableMinimizedByFinalizer(
                cost_dimension.CumulVar(self.routing.End(i)))
        
        # Define Transportation Requests.
        for order in orders:
            pickup_index = self.manager.NodeToIndex(self.order_to_pickup_node(order))
            dropoff_index = self.manager.NodeToIndex(self.order_to_dropoff_node(order))

            self.routing.AddPickupAndDelivery(pickup_index, dropoff_index)

            self.routing.solver().Add(self.routing.VehicleVar(pickup_index) == self.routing.VehicleVar(dropoff_index))

            # pickup before dropoff
            self.routing.solver().Add(time_dimension.CumulVar(pickup_index) < time_dimension.CumulVar(dropoff_index))
            
        # Allow to ignore orders, penalty
        for order in orders:
            self.routing.AddDisjunction([self.manager.NodeToIndex(self.order_to_pickup_node(order))], order['payment'] // 2)
            self.routing.AddDisjunction([self.manager.NodeToIndex(self.order_to_dropoff_node(order))], order['payment'] - order['payment'] // 2)
            
    def order_to_pickup_node(self, order):
        return self.pickup_id_to_node[order['pickup_point_id']]

    def order_to_dropoff_node(self, order):
        return self.dropoff_id_to_node[order['dropoff_point_id']]

    def depot_to_node(self, depot):
        return self.depot_id_to_node[depot['point_id']]

    def courier_to_node(self, courier):
        return self.courier_id_to_node[courier['courier_id']]
        
    def time_callback(self, from_index, to_index):
        """Returns the manhattan distance between the two nodes."""
        
        dist = self.dist_matrix[self.manager.IndexToNode(from_index), self.manager.IndexToNode(to_index)]
        if not self.routing.IsStart(to_index) and not self.routing.IsEnd(to_index):
            dist += 10
        return dist
        
#     def cost_callback(self, from_index, to_index):
#         """Returns the manhattan distance between the two nodes."""
#         # Convert from routing variable Index to distance matrix NodeIndex.
#         return self.dist_payment_matrix[self.manager.IndexToNode(from_index)][self.manager.IndexToNode(to_index)]
    
    def solve(self):
        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.solution_limit = 1
        search_parameters.time_limit.seconds = 180
#         search_parameters.lns_time_limit.seconds = 1
        search_parameters.savings_parallel_routes = True

        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC)

        # Solve the problem.
        assignment = self.routing.SolveWithParameters(search_parameters)
        return assignment
    
    def is_dropoff_node(self, node):
        return node >= 1 + len(self.couriers) + len(self.orders)
    
    def get_routes(self, assignment, verbose=True):
        """Get routes from assignment."""
        total_time = 0
        total_dropped = 0
        courier_routes = defaultdict(lambda: [])
        
        courier_start_time = {}
        courier_end_time = {}
        courier_dropped = defaultdict(lambda: 0)
        
        time_dimension = self.routing.GetDimensionOrDie('Time')
        for courier_index in range(len(self.couriers)):
            start_index = self.routing.Start(courier_index)
            index = start_index
            
            courier_routes[courier_index].append(index)
            plan_output = 'Route for courier {}:\n'.format(courier_index)
            route_time = 0
            
            while not self.routing.IsEnd(index):
                
                plan_output += ' {} -> '.format(self.manager.IndexToNode(index))
                previous_index = index
                index = assignment.Value(self.routing.NextVar(previous_index))
                courier_routes[courier_index].append(self.manager.IndexToNode(index))
                  
#                 route_time += self.routing.GetArcCostForVehicle(
#                     previous_index, index, courier_index)
                
                route_time += assignment.Value(time_dimension.CumulVar(index)) - assignment.Value(time_dimension.CumulVar(previous_index))
    
                if self.is_dropoff_node(self.manager.IndexToNode(index)):
                    courier_dropped[courier_index] += 1
                    total_dropped += 1
    
            courier_start_time[courier_index] = assignment.Value(time_dimension.CumulVar(start_index))
            courier_end_time[courier_index] = assignment.Value(time_dimension.CumulVar(index))  
            
#             courier_start_wait_time[courier_index] = assignment.Max(time_dimension.SlackVar(start_index))
            plan_output += '{}\n'.format(self.manager.IndexToNode(index))
            plan_output += 'Cost of the route: {}m\n'.format(route_time)
            if verbose and previous_index != self.routing.Start(courier_index):
                print(plan_output)
            total_time += route_time
        if verbose:
            print('Total Cost of all routes: {}m, Fractions of orders dropped off: {}'.format(
                total_time, total_dropped / len(self.orders)))
        return {courier_index: {'route': route[:-1], 
                                'start_time': courier_start_time[courier_index],
                                'end_time': courier_end_time[courier_index], 
                                'orders': courier_dropped[courier_index]
                                } 
                for courier_index, route in courier_routes.items() if len(route) > 2}

def get_node_action(courier, node, orders):
    n = len(orders)
    point_id = 'pickup_point_id' if node < n else 'dropoff_point_id'
    action = 'pickup' if node < n else 'dropoff'
    node = node if node < n else node - n
    return {'courier_id': courier['courier_id'], 'action': action, 
            'order_id': orders[node]['order_id'], 'point_id': orders[node][point_id]}


def get_solution(couriers, orders, depots, clusters):

    solution = []
    
    pb = tqdm(total=len(clusters))
    
    orders_complete = 0
    while(len(clusters) > 0):
        
        
        cluster_id = 0 #np.random.randint(0, len(clusters))
        cluster = clusters[cluster_id]
        pb.set_description(f"Cluster size: {len(cluster)}, Orders complete: {orders_complete}")
        
        cluster_orders = [orders[i] for i in cluster]
        solver = ORToolsSolver(couriers, cluster_orders, depots)
        assignment = solver.solve()
        
        if assignment:
            clusters.pop(cluster_id)
        else:
            continue

        cluster_routes = solver.get_routes(assignment)

        
        # update courier time window and starting node according to last destination
        for courier_index, courier_info in cluster_routes.items():
            old_courier_info = copy.deepcopy(couriers[courier_index])
            couriers[courier_index]['from'] = courier_info['end_time']
            
            end_node = courier_info['route'][-1] - len(couriers) - 1
            end_node = end_node if end_node < len(cluster_orders) else end_node - len(cluster_orders)
            
            # google doesn't accumulate waiting time!!!
            couriers[courier_index]['from'] = max(orders[cluster[end_node]]['dropoff_from'], couriers[courier_index]['from'])

            couriers[courier_index]['location_x'] = orders[cluster[end_node]]['dropoff_location_x']
            couriers[courier_index]['location_y'] = orders[cluster[end_node]]['dropoff_location_y']
            
            orders_complete += courier_info['orders']
            print(f"Courier changed: {old_courier_info} -> {couriers[courier_index]}")
#             if old_courier_info['courier_id'] == 114:
#                 import pdb; pdb.set_trace()
            

        cluster_solution = [get_node_action(couriers[courier_index], node - len(couriers) - 1, cluster_orders) 
                            for courier_index, courier_info in cluster_routes.items() for node in courier_info['route'][1:]
                            ]
        print(cluster_solution)
        pb.update(1)
        solution.extend(cluster_solution)

            
    return solution