from environment import Environment

import torch

env = Environment()

#couriers, orders, reward = env.main_logic()
#print(couriers, orders, reward)


'''courier_coords = torch.FloatTensor(list([[couriers[courierd_id].location_x, courier.location_y] for courier_id in couriers])).cuda()#dynamic
orders_coords = torch.FloatTensor(
    list([[order.pickup_location_x, order.pickup_location_y, order.dropoff_location_x, order.dropoff_location_y]
          for order in orders])).cuda()#static
orders_time = torch.FloatTensor(
    list([[order.pickup_from, order.pickup_to, order.dropoff_from, order.dropoff_to] for order in orders])).cuda()#static'''


action1 = [[1, 'pickup'],[]]
couriers, orders, reward = env.main_logic(action1)
print(couriers, orders, reward)
action2 = [[1, 'dropoff'],[]]
couriers, orders, reward = env.main_logic(action2)
print(couriers, orders, reward)
action3 = [[],[1,'pickup']]
couriers, orders, reward = env.main_logic(action3)
print(couriers, orders, reward)
action4 = [[],[1,'dropoff']]
couriers, orders, reward = env.main_logic(action4)
print(couriers, orders, reward)
'''dynamic = []


action1 = [[1, 'pick'],[0,'pick']]
observ1, reward1, done1 = env.step(action1)
print(observ1)'''