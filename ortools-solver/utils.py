# Manhattan
def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def order_distance(order):
    return manhattan_distance(order['pickup_location_x'], order['pickup_location_y'],
                              order['dropoff_location_x'], order['dropoff_location_y'])