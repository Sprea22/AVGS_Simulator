import random as rd
import pandas as pd
import numpy as np

##############################################################################
# The "new_goal" function is used by the free AGV in order to get new goals
# It allows to return different kind of goals considering the behavir type of
# the AGV within the simultion.
##############################################################################
def new_goal(ag, orders_list, behavior_type, n_col_per_ag, max1, max2):
    # Cambia in base al behavior type inserito E DISPONIBILITA' GATE
    for index, row in orders_list[orders_list["status"] == 1].iterrows():
        if(sum(row[2:]) == 0):
            orders_list["status"].iloc[index] = 2

    if(not(orders_list.loc[orders_list["status"] == 0].empty)):
        info_order = [-1, -1]

        if(behavior_type == 1):
            order, client, info_order, orders_list = getGoal_1(ag, orders_list)

        elif(behavior_type == 2):
            order, client, orders_list = getGoal_2(ag, orders_list, n_col_per_ag)

        elif(behavior_type == 3):
            ag, orders_list = getGoal_3(ag, orders_list)

        return  order, client, info_order, orders_list

    else:
        return [], [], [-1, -1], orders_list


##############################################################################
# The "new_gate" function is used by the AGV in order to get the gate location
# once they already picked up an article. The gate location depends by the client
# INPUT: agent, in particular ag.clients[0] that contains the current client for the agent
# OUTPUT: gate location
##############################################################################
def new_gate(ag, gates):
    if(ag.clients[0] == "A"):
        lp = gates[0].lp_hold()
        gate = 0
    elif(ag.clients[0] == "B"):
        lp = gates[1].lp_hold()
        gate = 1
    elif(ag.clients[0] == "C"):
        lp = gates[2].lp_hold()
        gate = 2
    else:
        print("Error - Client is not existing")
    return lp, gate, gates

def free_gate(ag, gates):
    gates[ag.gate].lp_free(ag.pos)
    return -1, gates

##############################################################################
# The "order_location" function allows to map the items location in the environment
# INPUT: an integer variable "ind"
# OUPUT: the location of the article in the "ind" position of the map_locations
##############################################################################
def order_location(ind):
    map_locations = {"shoes_R": (35,7), "shoes_G": (11,7), "shoes_B": (20,13), "tshirt_R" : (28,16), "tshirt_G" : (40,16), "tshirt_B" : (28,23),
    "pullover_R" : (19,26), "pullover_G" : (31,33), "pullover_B" : (15,33), "hat_R" : (42,36), "hat_G" : (24,42), "hat_B" : (45,41)}
    for i in map_locations.keys():
        if(i == ind):
            return map_locations[i]

##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

def getGoal_1(ag, orders_list):
    if(ag.info_order[0] != -1 and sum(orders_list.iloc[ag.info_order[0]][2:]) == 0):
        ag.info_order[0] = -1
    if(ag.info_order[0] == -1):
        ag.info_order[0] = orders_list.loc[orders_list["status"] == 0].iloc[0].name
        orders_list["status"].iloc[ag.info_order[0]] = 1
        window_order_list = orders_list.iloc[ag.info_order[0]]
    elif(ag.info_order[0] != -1):
        window_order_list = orders_list.iloc[ag.info_order[0]]

    window_order_list = window_order_list.to_frame().T
    window_order_list.index = range(0,1)
    order, client, window_order_list = getGoal(ag, window_order_list)
    orders_list.iloc[ag.info_order[0]] = window_order_list.iloc[0]
    return  order, client, ag.info_order, orders_list



def getGoal_2(ag, orders_list, n_col_per_ag):
    # Si può mettere nell'inizializzazione degli AGV una volta sola nel main
    ag_columns = ["client", "status"]
    for x in orders_list.columns[ag.id : ag.id + n_col_per_ag]:
        ag_columns.append(x)
    order, client, window_orders_list = getGoal(ag, orders_list[ag_columns])
    orders_list[ag_columns] = window_orders_list
    return order, client, orders_list



def getGoal(ag, window_orders_list):
    if(len(window_orders_list) != 0):
        clients = window_orders_list["client"]
        order = []
        client = []
        for index, row in window_orders_list.iterrows():
            for column in window_orders_list:
                if(column != "client" and column != "status"):
                    if(row[column] == 1):
                         order.append(order_location(column))
                         client.append(clients[index])
                         window_orders_list[column].iloc[index] = 0
                         print("----------", order, client)
                         return order, client, window_orders_list
        return [], [], window_orders_list
