class Courier:
    courier_id = None
    location_x = None
    location_y = None
    # order_info хранит [tuple(courier_id, action), tuple(courier_id, action)]
    order_info = []
    has_order = False
