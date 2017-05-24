import re

b_chromosome_new_str_list = []
s_chromosome_new_str_list = []
    
with open ('conserved_best_chromosome.txt', 'r') as f:

    for line in f:
        if line == '\n':
            continue
        buy_or_sell = re.findall(r'_day_([A-Za-z]+)#', line)[0]
        chromosome_str = re.findall(r'chromosome#([0-9]+)#', line)[0]
        chromosome_list = list(chromosome_str)
        chromosome_new_str = ",".join(chromosome_list)
        if buy_or_sell == "buy":
            b_chromosome_new_str_list.append(chromosome_new_str)
        elif buy_or_sell == "sell":
            s_chromosome_new_str_list.append(chromosome_new_str)
    
    
with open ("c_buy_chromosome.txt".format(buy_or_sell), 'w') as f:
    for s in b_chromosome_new_str_list:
        f.write(s + "---------[28]\n")
    
with open ("c_sell_chromosome.txt".format(buy_or_sell), 'w') as f:
    for s in s_chromosome_new_str_list:
        f.write(s + "---------[28]\n")