\* Beer Distribution Problem *\
Minimize
Sum_of_Transporting_Costs: 2 route_A_1 + 4 route_A_2 + 5 route_A_3
 + 2 route_A_4 + route_A_5 + 3 route_B_1 + route_B_2 + 3 route_B_3
 + 2 route_B_4 + 3 route_B_5
Subject To
Sum_of_Products_into_Bar1: route_A_1 + route_B_1 >= 500
Sum_of_Products_into_Bar2: route_A_2 + route_B_2 >= 900
Sum_of_Products_into_Bar3: route_A_3 + route_B_3 >= 1800
Sum_of_Products_into_Bar4: route_A_4 + route_B_4 >= 200
Sum_of_Products_into_Bar5: route_A_5 + route_B_5 >= 700
Sum_of_Products_out_of_Warehouse_A: route_A_1 + route_A_2 + route_A_3
 + route_A_4 + route_A_5 <= 1000
Sum_of_Products_out_of_Warehouse_B: route_B_1 + route_B_2 + route_B_3
 + route_B_4 + route_B_5 <= 4000
Bounds
0 <= route_A_1
0 <= route_A_2
0 <= route_A_3
0 <= route_A_4
0 <= route_A_5
0 <= route_B_1
0 <= route_B_2
0 <= route_B_3
0 <= route_B_4
0 <= route_B_5
Generals
route_A_1
route_A_2
route_A_3
route_A_4
route_A_5
route_B_1
route_B_2
route_B_3
route_B_4
route_B_5
End
