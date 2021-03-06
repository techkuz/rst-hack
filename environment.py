from n_parser import Parser
from courier import Courier

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
            self.orders_payment = 0
            self.profit = 0
            self.time = self.START_MINUTES

    def new_action(self, actions: list) -> None :
        # На вход приходит лист из новых actions
        # Формат: [[c_id, action], [c_id, action]]
        for order_idx, action_data in enumerate(actions):
            if action_data:
                courier_id, action = action_data
                self.couriers[courier_id].order_info.append((order_idx+10001, action))

    def return_valuable_info(self) -> tuple:
        couriers_locations = [[courier['location_x'], courier['location_y']] for courier in self.couriers]
        return self.orders, couriers_locations, self.couriers

    def main_logic(self, action=None):
        if action:
            new_actions = self.new_action(action)

        work_duration=0

        action_done = False
        for courier_id in self.couriers:
            if self.couriers[courier_id].order_info:
                courier_order = self.couriers[courier_id].order_info[0][0]
                courier_action = self.couriers[courier_id].order_info[0][1]
                print(courier_id,courier_order,courier_action,self.couriers[courier_id].order_info)

                if courier_action == 'pickup':
                    distance = Courier.get_travel_duration_minutes([self.couriers[courier_id].location_x,
                                                                    self.couriers[courier_id].location_y],
                                                                   [self.orders[courier_order].pickup_location_x,
                                                                    self.orders[courier_order].pickup_location_y])
                    print('pick dist')
                    self.couriers[courier_id].destination_distance = distance
                    #print(courier_id,distance)
                elif courier_action == 'dropoff':
                    distance = Courier.get_travel_duration_minutes([self.couriers[courier_id].location_x,
                                                                    self.couriers[courier_id].location_y],
                                                                   [self.orders[courier_order].dropoff_location_x,
                                                                    self.orders[courier_order].dropoff_location_y])
                    self.couriers[courier_id].destination_distance = distance
        # итерируюсь по минутам рабочего времени курьеров
        for minute in range(self.time, self.END_MINUTES+1):
            #self.time +=1
            #print(minute)
            if action_done:
                self.time = minute
                break
            for courier_id in self.couriers:
                if self.couriers[courier_id].destination_distance == 0:
                    action_done = True
                    continue
                if not self.couriers[courier_id].order_info:
                    continue
                courier_action = self.couriers[courier_id].order_info[0][1]
                courier_order = self.couriers[courier_id].order_info[0][0]

                self.couriers[courier_id].time += 1
                if self.couriers[courier_id].destination_distance is not None:
                    self.couriers[courier_id].destination_distance -= 1
                if courier_action == 'pickup':
                    work_duration = Courier.get_travel_duration_minutes([self.couriers[courier_id].location_x,
                                                                    self.couriers[courier_id].location_y],
                                                                   [self.orders[courier_order].pickup_location_x,
                                                                    self.orders[courier_order].pickup_location_y])
                    self.couriers[courier_id].location_x = self.orders[self.couriers[courier_id].order_info[0][0]].pickup_location_x
                    self.couriers[courier_id].location_y = self.orders[self.couriers[courier_id].order_info[0][0]].pickup_location_y
                    if self.orders[courier_order].pickup_from < minute < self.orders[courier_order].pickup_to:
                        action = self.couriers[courier_id].order_info.pop()
                        self.couriers[courier_id].has_order = True
                    work_payment = work_duration * 2
                    self.profit -= work_payment

                elif courier_action == 'dropoff':
                    work_duration = Courier.get_travel_duration_minutes([self.couriers[courier_id].location_x,
                                                                    self.couriers[courier_id].location_y],
                                                                   [self.orders[courier_order].dropoff_location_x,
                                                                    self.orders[courier_order].dropoff_location_y])
                    self.couriers[courier_id].location_x = self.orders[
                        self.couriers[courier_id].order_info[0][0]].dropoff_location_x
                    self.couriers[courier_id].location_y = self.orders[
                        self.couriers[courier_id].order_info[0][0]].dropoff_location_y
                    if self.orders[courier_order].dropoff_from < minute < self.orders[courier_order].dropoff_to:
                        self.orders_payment = self.orders[courier_order].payment
                        self.orders[self.couriers[courier_id].order_info[0][0]].delivered = True
                        action = self.couriers[courier_id].order_info.pop()
                        self.couriers[courier_id].has_order = False

                        if not self.couriers[courier_id].order_info:
                            self.couriers[courier_id].is_active = False
                    work_payment = work_duration*2
                    self.profit += self.orders_payment - work_payment

        #work_duration = sum([x.time - 360 for x in self.couriers.values()])
        return self.couriers, self.orders, self.profit


if __name__ == '__main__':
    env = Environment()