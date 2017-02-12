# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import sys
import random







def cross_over(p1, p2, mode = 'uniform'):

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
        random_point = random.randint(0, len(p1)-1)
        c1 = p1[0:random_point] + p2[random_point:len(p2)]
        c2 = p2[0:random_point] + p1[random_point:len(p2)]
        return c1, c2

    @accepts(list, list)
    def multi_point(p1, p2):
        sample_list = list(range(1,len(p1)-1))
        sample_num = random.randint(2, len(sample_list))
        random_points = random.sample(sample_list, sample_num)
        random_points = sorted(random_points)
        c1 = []
        c2 = []
        for i, point in enumerate(random_points):
            # start point
            if i == 0:
                c1.extend(p1[0:point])
                c2.extend(p2[0:point])
            # end point
            elif i == len(random_points)-1 and i % 2 != 0:
                c1.extend(p1[point:len(p1)])
                c2.extend(p1[point:len(p2)])
            elif i == len(random_points) - 1 and i % 2 == 0:
                c1.extend(p2[point:len(p2)])
                c2.extend(p2[point:len(p1)])
            # middle points
            elif i % 2 == 0:
                c1.extend(p2[random_points[i-1]:point])
                c2.extend(p1[random_points[i-1]:point])
            elif i % 2 != 0:
                c1.extend(p1[random_points[i-1]:point])
                c2.extend(p2[random_points[i-1]:point])
        return c1, c2

    @accepts(list, list)
    def uniform(p1, p2):
        random_list = [0,1]
        c1 = p1[:]
        c2 = p2[:]
        for i, cell in enumerate(c1):
            is_filp = random.sample(random_list,1)
            if is_filp:
                c1[i],c2[i] = c2[i],c1[i]
        return c1, c2

    #:::Crossover:::
    input_list_length_check(p1, p2)
    mode_dict = {
                "one_point": one_point,
                "multi_point": multi_point,
                "uniform": uniform,
                 }

    return mode_dict[mode](p1,p2)