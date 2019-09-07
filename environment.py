from parser import Parser


class Environment:
    # 6 AM
    START_MINUTES = 360

    # 23:59
    END_MINUTES = 1439

    START_FILE = 'simple_input.json'

    def __init__(self, file: str = START_FILE):
         with open(file, 'r') as file:
            parser = Parser(data=file)

            self.couriers = parser.get_couriers()
            self.depots = parser.get_depots()
            self.orders = parser.get_orders()

    def logic(self, actions: list):
        # [[c_id, action], [c_id, action]] list idx is an order number
        for order_id, c_id, action in enumerate(actions):
            self.couriers[c_id].order_info.append((order_id, action))

    def main_logic(self):
        dummy_actions = []
        new_actions = self.logic(dummy_actions)

        # итерируюсь по минутам рабочего времени курьеров
        for minute in range(self.START_MINUTES, self.END_MINUTES+1, 1):
            for courier in self.couriers:
                courier_action = courier.order_info[0][1]
                courier_order = courier.order_info[0][0]

                if courier_action == 'pick':
                    if courier_order.pickup_from < minute < courier_order.pickup_to:
                        action = courier.order_info.pop()
                        courier.has_order = True
                        # order = courier.orders.pop()
                elif courier_action == 'drop':
                    if courier_order.dropoff_from < minute < courier_order.dropoff_to:
                        action = courier.order_info.pop()
                        courier.has_order = False


if __name__ == '__main__':
    env = Environment()