def m_i(distance_list):
    fitness = 7.5
    for distance in distance_list:
        new_fitness = fitness * distance
        print (distance, new_fitness)

distance_list = [x*0.01 for x in range(200)]
m_i(distance_list)
