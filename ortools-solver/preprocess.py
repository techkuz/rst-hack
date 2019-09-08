import numpy as np

from utils import manhattan_distance

def preprocess_data(couriers, orders):

    impossible_orders = 0
    filtered_orders = []
    for order in orders:
        distance = manhattan_distance(order['pickup_location_x'], order['pickup_location_y'], 
                                      order['dropoff_location_x'], order['dropoff_location_y'])

        closest_courier = None
        closest_courier_distance = np.inf
        for courier in couriers:
            courier_distance = manhattan_distance(courier['location_x'], courier['location_y'], 
                                                  order['pickup_location_x'], order['pickup_location_y'])

            if courier_distance < closest_courier_distance:
                closest_courier = courier
                closest_courier_distance = courier_distance

        max_window = order['dropoff_to'] - max(order['pickup_from'], 360 + closest_courier_distance)

        if distance >= max_window:
            impossible_orders += 1
        else:
            filtered_orders.append(order)

    print(f"Total orders: {len(orders)}, Impossible without depot: {impossible_orders}")
    
    
    # fix order's time windows
    bad_order_counter = 0
    for order in filtered_orders:
        if order['pickup_to'] <= order['pickup_from']:
            print(f"Bad time window order: {(order['pickup_from'], order['pickup_to'])}")
            order['pickup_to'], order['pickup_from'] = order['pickup_from'], order['pickup_to']
            bad_order_counter += 1

        if order['dropoff_to'] <= order['dropoff_from']:
            print(f"Bad time window order: {(order['dropoff_from'], order['dropoff_to'])}")
            order['dropoff_to'], order['dropoff_from'] = order['dropoff_from'], order['dropoff_to']
            bad_order_counter += 1
    
    # courier initial time windows
    for i, courier in enumerate(couriers):
        courier['from'] = 6 * 60
        courier['to'] = 24 * 60
    
    return couriers, filtered_orders