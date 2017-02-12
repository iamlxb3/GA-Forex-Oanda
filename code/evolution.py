# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import sys
import random

class CrossOver():
    def __init__(self, parameter_dict):
        self.mode = parameter_dict['evolution']['cross_over']['mode']

    def __call__(self, p1, p2):
        def input_list_length_check(p1, p2):
            # check the length of both parents
            if len(p1) != len(p2):
                logger1.error("The length of the input parents for the crossover is not equal!!")
                logger1.error("Error parent list: ", p1)
                logger1.error("Error parent list: ", p2)
                sys.exit(0)

        # p1 -> parent1
        @accepts(list, list)
        def one_point(p1, p2):
            # select the random point
            random_point = random.randint(1, len(p1)-1)
            c1 = p1[0:random_point] + p2[random_point:len(p2)]
            c2 = p2[0:random_point] + p1[random_point:len(p2)]
            return c1, c2

        @accepts(list, list)
        def multi_point(p1, p2):
            sample_list = list(range(1,len(p1)-1))
            # [0,1,2,3,4], sample_num  = 4, sample_num indicate the num of gap, eg. the first sample_num 1 is the gap
            # between 0 and 1
            sample_num = random.randint(1, len(sample_list)-1)
            random_points = random.sample(sample_list, sample_num)
            cut_point_list = random_points[:]
            cut_point_list.extend([0, len(p1)])
            cut_point_list = sorted(cut_point_list)
            # cut_point_list = [0,2,3,8], cut_point_list = [2,3,8]
            #cut_point_tuple_list [(0, 2), (2, 3), (3, 8)]
            cut_point_tuple_list = list(zip(cut_point_list, cut_point_list[1:]))
            print ("cut_point_tuple_list", cut_point_tuple_list)
            c1 = p1[:]
            c2 = p2[:]
            for i, edge_tuple in enumerate(cut_point_tuple_list):
                # only flip those odd parts
                if i % 2 == 0:
                    continue
                e0 = edge_tuple[0]
                e1 = edge_tuple[1]
                c1[e0:e1], c2[e0:e1] = c2[e0:e1], c1[e0:e1]
            print (c1,c2)
            return c1, c2

        @accepts(list, list)
        def uniform(p1, p2):
            random_list = [0,1]
            c1 = p1[:]
            c2 = p2[:]
            for i, cell in enumerate(c1):
                is_filp = random.sample(random_list,1)[0]
                if is_filp:
                    c1[i],c2[i] = c2[i],c1[i]
            return c1, c2

        #:::Crossover:::
        mode = self.mode
        input_list_length_check(p1, p2)
        mode_dict = {
                    "one_point": one_point,
                    "multi_point": multi_point,
                    "uniform": uniform,
                     }

        return mode_dict[mode](p1,p2)


class Mutation():

    def __init__(self, parameter_dict):
        self.flip_bit_num = parameter_dict['evolution']['mutation']['flip_bit_num']
        self.mode = parameter_dict['evolution']['mutation']['mode']

    def __call__(self, individual):
        mode = self.mode
        flip_bit_num = self.flip_bit_num

        @accepts(list)
        def random_flip(individual):
            list_length = len(individual)
            random_list = list(range(0, list_length))
            flip_bits = random.sample(random_list, flip_bit_num)
            for flip_bit in flip_bits:
                old_bit_value = individual[flip_bit]
                if old_bit_value == 0:
                    individual[flip_bit] = 1
                elif old_bit_value == 1:
                    individual[flip_bit] = 0
            return individual

        @accepts(list)
        def bit_flip(individual):
            list_length = len(individual)
            random_list = list(range(0, list_length))
            flip_bit = random.sample(random_list, 1)[0]
            old_bit_value = individual[flip_bit]
            if old_bit_value == 0:
                individual[flip_bit] = 1
            elif old_bit_value == 1:
                individual[flip_bit] = 0
            return individual

        mode_dict = {
                    "random_flip": random_flip,
                    "bit_flip": bit_flip,
        }
        return mode_dict[mode](individual)
