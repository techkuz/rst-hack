import json

ACTION = ['PICK', 'DROP']

# 6 AM
START_MINUTES = 360

# 23:59
END_MINUTES = 1439

FILE = 'simple_input.json'


class Courier:
    courier_id = None
    location_x = None
    location_y = None
    status = 'FREE'
    actions = []
    orders = []
    has_order = False


class Depot:
    point_id = None
    location_x = None
    location_y = None


class Order:
    order_id = None
    pickup_point_id = None
    pickup_location_x = None
    pickup_location_y = None
    pickup_from = None
    pickup_to = None
    dropoff_point_id = None
    dropoff_location_x = None
    dropoff_location_y = None
    dropoff_from = None
    dropoff_to = None
    payment = None


def init_start(file):
    with open(FILE, 'r') as file:
        data = json.load(file)
        # print(data)
        couriers = {}
        for courier in data['couriers']:
            new_courier = Courier()
            new_courier.courier_id = courier.get('courier_id')
            new_courier.location_x = courier.get('location_x')
            new_courier.location_y = courier.get('location_y')
            couriers[new_courier.courier_id] = new_courier

        depots = {}
        for depot in data['depots']:
            new_depot = Depot()
            new_depot.point_id = depot.get('point_id')
            new_depot.location_x = depot.get('location_x')
            new_depot.location_y = depot.get('location_y')
            depots[new_depot.point_id] = new_depot

        orders = {}
        for order in data['orders']:
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

        res = {'couriers': couriers, 'depots': depots, 'orders': orders}
        return res


def logic(couriers, depots, orders, actions: list):
    # [[c_id, action], [c_id, action]] list idx is an order number
    for order_id, c_id, action in enumerate(actions):
        couriers[c_id].actions.append(action)
        couriers[c_id].orders.append(order_id)

    return couriers


if __name__ == '__main__':
    initial_data = init_start(file=FILE)
    couriers = initial_data.get('couriers')
    depots = initial_data.get('depots')
    orders = initial_data.get('orders')

    actions = []
    new_actions = logic(couriers, depots, orders, actions)

    # итерируюсь по минутам рабочего времени курьеров
    for minute in range(START_MINUTES, END_MINUTES+1, 1):
        for courier in couriers:
            if courier.actions[0] == 'pick':
                if minute > courier.orders[0].pickup_from and minute < courier.orders[0].pickup_to:
                    action = courier.actions.pop()
                    courier.has_order = True
                    # order = courier.orders.pop()
            elif courier.actions[0] == 'drop':
                if minute > courier.orders[0].dropoff_from and minute < courier.orders[0].dropoff_to:
                    action = courier.actions.pop()
                    courier.has_order = False
                    order = courier.orders.pop()

