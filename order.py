class Order:
    def __init__(self):
        self.order_id = None
        self.pickup_point_id = None
        self.pickup_location_x = None
        self.pickup_location_y = None
        self.pickup_from = None
        self.pickup_to = None
        self.dropoff_point_id = None
        self.dropoff_location_x = None
        self.dropoff_location_y = None
        self.dropoff_from = None
        self.dropoff_to = None
        self.payment = None
        # доставлен
        self.delivered = False