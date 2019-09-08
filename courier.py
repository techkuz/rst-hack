class Courier:
    courier_id = None
    location_x = None
    location_y = None
    # order_info хранит [tuple(order_id, action), tuple(order_id, action)]
    order_info = []
    has_order = False
    # не закончил работу
    is_active = True
    time = 360
    destination_distance = None

    @classmethod
    def get_travel_duration_minutes(cls, location1, location2):
        """Время перемещения курьера от точки location1 до точки location2 в минутах"""
        distance = abs(location1[0] - location2[0]) + abs(location1[1] - location2[1])
        return distance
