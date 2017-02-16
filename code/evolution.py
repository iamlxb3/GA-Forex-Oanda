# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import sys
import random
import bisect
from solution import Solution

class OffspringGeneration():
    def __init__(self, parameter_dict):
        self.max_population_num = parameter_dict['SGA']['max_population_num']
        self.parent_select_mode = parameter_dict['SGA']['parent_select_mode']
        self.TS_K = parameter_dict['SGA']['TS']['TS_K']
        self.parameter_dict = parameter_dict

    def parent_selection(self, compare_tuple_list):
        # TODO fix the bug of "population larger than sample"
        def tournament_selection(compare_tuple_list):
            sp1_random_list = random.sample(compare_tuple_list, self.TS_K)
            sp1_tuple = sorted(sp1_random_list, key = lambda x:x[1], reverse = True)[0]
            compare_tuple_list.remove(sp1_tuple)
            sp2_random_list = random.sample(compare_tuple_list, self.TS_K)
            sp2_tuple = sorted(sp2_random_list, key = lambda x:x[1], reverse = True)[0]
            sp1 = sp1_tuple[0]
            sp2 = sp2_tuple[0]
            logger1.debug("chosen_K:{}".format(self.TS_K))
            logger1.debug("parent1 name: {}, chromosome_bits:{}, fitness:{}, parent2 name: {}, chromosome_bits:{}, fitness:{},"
                          .format(sp1.name, sp1.chromosome_bits, sp1.fitness, sp2.name, sp2.chromosome_bits, sp2.fitness))
            logger1.debug(":::tournament parent selection complete:::!")
            return sp1, sp2

        def roulette_wheel_selection(compare_tuple_list):

            def get_parent_index(solution_probability_list, solution_list):
                chosen_parent_index = bisect.bisect(solution_probability_list, random.random())
                return chosen_parent_index

            #:::roulette_wheel_selection:::
            sorted_compare_tuple_list = sorted(compare_tuple_list, key = lambda x:x[1], reverse = True)
            unzip_sorted_compare_tuple_list = [xy for xy in zip(*sorted_compare_tuple_list)]
            solution_list = unzip_sorted_compare_tuple_list[0]
            solution_fitness_list = unzip_sorted_compare_tuple_list[1]
            # convert the fitness to the possibility of being chosen eg: [0.4, 0.3, 0.2, 0.1]
            solution_probability_list = [float("{:.3f}".format(x/sum(solution_fitness_list))) for x in solution_fitness_list]
            # [0.4, 0.3, 0.2, 0.1] -> [0.4, 0.7, 0.9, 1.0]
            for i, x in enumerate(solution_probability_list):
                if i > 0:
                    solution_probability_list[i] += solution_probability_list[i - 1]
            logger1.debug("solution_probability_list:{}".format(solution_probability_list))
            logger1.debug("solution_list:{}".format([solution.name for solution in solution_list]))
            sp1_index = get_parent_index(solution_probability_list, solution_list)
            sp2_index = get_parent_index(solution_probability_list, solution_list)
            while sp1_index == sp2_index:
                sp2_index = get_parent_index(solution_probability_list, solution_list)
            sp1 = solution_list[sp1_index]
            sp2 = solution_list[sp2_index]
            logger1.debug("parent1 selected name:{}, parent2 selected name:{}".format(sp1.name, sp2.name))
            logger1.debug("parent1 name: {}, chromosome_bits:{}, fitness:{}, parent2 name: {}, chromosome_bits:{}, fitness:{},"
                          .format(sp1.name, sp1.chromosome_bits, sp1.fitness, sp2.name, sp2.chromosome_bits, sp2.fitness))
            logger1.debug(":::roulette wheel parent selection complete:::!")
            return sp1, sp2

        # :::parent_selection:::
        parent_select_mode_dict = {
                                    "TS":tournament_selection,
                                    "RWS":roulette_wheel_selection,
        }
        return parent_select_mode_dict[self.parent_select_mode](compare_tuple_list)

    def __call__(self, parents_list):


        #:::__call__
        temp_offsprings_pool = []
        population_now = len(parents_list)
        compare_tuple_list = [(parent, parent.fitness) for parent in parents_list]
        while population_now <= self.max_population_num-2:
            compare_tuple_list_copy = compare_tuple_list.copy()
            logger1.debug("===============START PARENT SELECTION===============")
            sp1, sp2 = self.parent_selection(compare_tuple_list_copy)
            sp1_chbits = sp1.chromosome_bits
            sp2_chbits = sp2.chromosome_bits
            logger1.debug("===============PARENT SELECTION END=================")
            # cross_over
            logger1.debug("===============CROSS OVER START=====================")
            cross_over = CrossOver(self.parameter_dict)
            c1_chbits, c2_chbits = cross_over(sp1_chbits, sp2_chbits)
            logger1.debug("===============CROSS OVER END=======================")
            # mutation
            logger1.debug("===============MUTATION START=======================")
            mutation = Mutation(self.parameter_dict)
            is_mutation = mutation.is_mutation()
            if is_mutation:
                c1_chbits = mutation(c1_chbits)
                c2_chbits = mutation(c2_chbits)
            logger1.debug("===============MUTATION END=========================")
            # create solution object
            c1 = Solution()
            c2 = Solution()
            c1.chromosome_bits = c1_chbits
            c2.chromosome_bits = c2_chbits
            temp_offsprings_pool.append(c1)
            temp_offsprings_pool.append(c2)
            # count entire population
            population_now += 2
            logger1.debug("child1 created name:{}, child2 created name:{}".format(c1.name, c2.name))
            if is_mutation:
                logger1.info("Mutation happened!! child1_name:{}, child2_name:{}".format(c1.name, c2.name))
            logger1.debug("child1 chromosome_bits:{}, child2 chromosome_bits:{}".format(c1.chromosome_bits, c2.chromosome_bits))
            logger1.debug("Two children have been created!!")
        logger1.debug("populaton pool is fool now, total solutions number : {}".format(population_now))


        return temp_offsprings_pool



class CrossOver():
    def __init__(self, parameter_dict):
        self.mode = parameter_dict['evolution']['cross_over']['mode']

    def __call__(self, p1_chbits, p2_chbits):
        def input_list_length_check(p1_chbits, p2_chbits):
            # check the length of both parents
            if len(p1_chbits) != len(p2_chbits):
                logger1.error("The length of the input parents for the crossover is not equal!!")
                logger1.error("Error parent list: ", p1_chbits)
                logger1.error("Error parent list: ", p2_chbits)
                sys.exit(0)

        # p1 -> parent1
        @accepts(list, list)
        def one_point(p1_chbits, p2_chbits):
            # select the random point
            random_point = random.randint(1, len(p1_chbits)-1)
            c1 = p1_chbits[0:random_point] + p2_chbits[random_point:len(p2_chbits)]
            c2 = p2_chbits[0:random_point] + p1_chbits[random_point:len(p2_chbits)]
            # logging
            logger1.debug("<<<one point mutation>>>")
            logger1.debug("chosen_point: {}".format(random_point))
            return c1, c2

        @accepts(list, list)
        def multi_point(p1_chbits, p2_chbits):
            sample_list = list(range(1,len(p1_chbits)-1))
            # [0,1,2,3,4], sample_num  = 4, sample_num indicate the num of gap, eg. the first sample_num 1 is the gap
            # between 0 and 1
            sample_num = random.randint(1, len(sample_list)-1)
            random_points = random.sample(sample_list, sample_num)
            cut_point_list = random_points[:]
            cut_point_list.extend([0, len(p1_chbits)])
            cut_point_list = sorted(cut_point_list)
            # cut_point_list = [0,2,3,8], cut_point_list = [2,3,8]
            #cut_point_tuple_list [(0, 2), (2, 3), (3, 8)]
            cut_point_tuple_list = list(zip(cut_point_list, cut_point_list[1:]))
            print ("cut_point_tuple_list", cut_point_tuple_list)
            c1 = p1_chbits[:]
            c2 = p2_chbits[:]
            for i, edge_tuple in enumerate(cut_point_tuple_list):
                # only flip those odd parts
                if i % 2 == 0:
                    continue
                e0 = edge_tuple[0]
                e1 = edge_tuple[1]
                c1[e0:e1], c2[e0:e1] = c2[e0:e1], c1[e0:e1]
            # logging
            logger1.debug("<<<one point mutation>>>")
            logger1.debug("chosen_points: {}".format(cut_point_list))
            logger1.debug("cut_parts: {}".format(cut_point_tuple_list))
            return c1, c2

        @accepts(list, list)
        def uniform(p1_chbits, p2_chbits):
            random_list = [0,1]
            c1 = p1_chbits[:]
            c2 = p2_chbits[:]
            # create for logging
            filped_points = []
            for i, cell in enumerate(c1):
                is_filp = random.sample(random_list,1)[0]
                if is_filp:
                    # logging purpose
                    filped_points.append(i)
                    c1[i],c2[i] = c2[i],c1[i]
            logger1.debug("<<<uniform>>>")
            logger1.debug("flipped_points: {}".format(filped_points))
            return c1, c2

        #:::Crossover:::
        mode = self.mode
        input_list_length_check(p1_chbits, p2_chbits)
        mode_dict = {
                    "one_point": one_point,
                    "multi_point": multi_point,
                    "uniform": uniform,
                     }

        return mode_dict[mode](p1_chbits,p2_chbits)


class Mutation():

    def __init__(self, parameter_dict):
        self.flip_bit_num = parameter_dict['evolution']['mutation']['flip_bit_num']
        self.mode = parameter_dict['evolution']['mutation']['mode']
        self.mutation_rate = float(parameter_dict['DSGA']['M'])

    def is_mutation(self):
        random_number = random.random()
        if random_number < self.mutation_rate:
            return True
        else:
            return False


    def __call__(self, chromosome_bits):
        mode = self.mode
        flip_bit_num = self.flip_bit_num

        @accepts(list)
        def random_flip(chromosome_bits):
            list_length = len(chromosome_bits)
            random_list = list(range(0, list_length))
            flip_bits = random.sample(random_list, flip_bit_num)
            for flip_bit in flip_bits:
                old_bit_value = chromosome_bits[flip_bit]
                if old_bit_value == 0:
                    chromosome_bits[flip_bit] = 1
                elif old_bit_value == 1:
                    chromosome_bits[flip_bit] = 0
            # logging
            logger1.debug("<<<random_flip>>>")
            logger1.debug("flip_bit_num: {}".format(flip_bit_num))
            logger1.debug("flipped_bits: {}".format(flip_bits))
            return chromosome_bits

        @accepts(list)
        def bit_flip(chromosome_bits):
            list_length = len(chromosome_bits)
            random_list = list(range(0, list_length))
            flip_bit = random.sample(random_list, 1)[0]
            old_bit_value = chromosome_bits[flip_bit]
            if old_bit_value == 0:
                chromosome_bits[flip_bit] = 1
            elif old_bit_value == 1:
                chromosome_bits[flip_bit] = 0
            # logging
            logger1.debug("<<<bit_flip>>>")
            logger1.debug("flipped_bit: {}".format(flip_bit))
            return chromosome_bits

        mode_dict = {
                    "random_flip": random_flip,
                    "bit_flip": bit_flip,
        }


        return mode_dict[mode](chromosome_bits)
