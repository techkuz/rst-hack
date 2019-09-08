class Courier:
    def __init__(self):
        self.courier_id = None
        self.location_x = None
        self.location_y = None
        # order_info хранит [tuple(order_id, action), tuple(order_id, action)]
        self.order_info = []
        self.has_order = False
        # не закончил работу
        self.is_active = True
        self.time = 360
        self.destination_distance = None

    @classmethod
    def get_travel_duration_minutes(cls, location1, location2):
        """Время перемещения курьера от точки location1 до точки location2 в минутах"""
        distance = abs(location1[0] - location2[0]) + abs(location1[1] - location2[1])
        return distance
