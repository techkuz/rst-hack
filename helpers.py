import json

from courier import Courier
from depot import Depot
from order import Order


class Parser:
    def __init__(self, data):
        self.data = json.load(data)

    def get_couriers(self) -> dict:
        couriers = {}
        for courier in self.data['couriers']:
            new_courier = Courier()
            new_courier.courier_id = courier.get('courier_id')
            new_courier.location_x = courier.get('location_x')
            new_courier.location_y = courier.get('location_y')
            couriers[new_courier.courier_id] = new_courier

        return couriers

    def get_depots(self) -> dict:
        depots = {}
        for depot in self.data['depots']:
            new_depot = Depot()
            new_depot.point_id = depot.get('point_id')
            new_depot.location_x = depot.get('location_x')
            new_depot.location_y = depot.get('location_y')
            depots[new_depot.point_id] = new_depot

        return depots

    def get_orders(self) -> dict:
        orders = {}
        for order in self.data['orders']:
            new_order = Order()
            new_order.order_id = order.get('order_id')
            new_order.pickup_point_id = order.get('pickup_point_id')
            new_order.pickup_location_x = order.get('pickup_location_x')
            new_order.pickup_location_y = order.get('pickup_location_y')
            new_order.pickup_from = order.get('pickup_from')
            new_order.pickup_to = order.get('pickup_to')
            new_order.dropoff_point_id = order.get('dropoff_point_id')
            new_order.dropoff_location_x = order.get('dropoff_location_x')
            new_order.dropoff_location_y = order.get('dropoff_location_y')
            new_order.dropoff_from = order.get('dropoff_from')
            new_order.dropoff_to = order.get('dropoff_to')
            new_order.payment = order.get('payment')
            orders[new_order.order_id] = new_order

        return orders
