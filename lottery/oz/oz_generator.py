import random
import time
from statistics import mean, pstdev

millis = int(round(time.time() * 1000))
random.seed(a = millis)

def random_draw():
    draw = {'nums': random_set()}
    supply_nums = set()
    while len(supply_nums) < 2:
        num = random.randint(1, 45)
        if num not in draw['nums']:
            supply_nums.add(num)
    draw['supps'] = sorted(list(supply_nums))

    return draw


def random_set(prefill =[]):
    result = set(prefill)
    while len(result) < 7:
        num = random.randint(1, 45)
        result.add(num)
    
    return sorted(list(result))

def system_set(size):
    result = set()
    while len(result) < size:
        num = random.randint(1, 45)
        result.add(num)
    
    return sorted(list(result))

def generate_ticket(size, conditions, prefills):
    ticket =[]
    time_out = 10000
    prefill_flatten = [num for prefill in prefills for num in prefill]
    while len(ticket) < size and time_out>0:
        nums = random_set(prefill_flatten)
        condition_results = [condition(nums) for condition in conditions]
        if all(condition_results):
            ticket.append(nums)
        time_out-=1
        # print(time_out)
    return ticket

def random_ticket(size):
    return [random_set() for i in range(size)]

def system_ticket(set_size, ticket_size):
    return [system_set(set_size) for i in range(ticket_size)]

def random_ticket_each():
    return [random_set([i+1]) for i in range(45)]

def random_ticket_with_neighbout_num(size):
    ticket =[]
    while len(ticket) < size:
        nums = random_set()
        nums_temp = [num+1 for num in nums]
        if len(set(nums) & set(nums_temp))>0:
            ticket.append(nums)
    return ticket

def random_ticket_with_lower_average(size):
    ticket =[]
    while len(ticket) < size:
        nums = random_set()
        
        if mean(nums)<23:
            ticket.append(nums)
    return ticket

def random_ticket_with_higher_average(size):
    ticket =[]
    while len(ticket) < size:
        nums = random_set()
        
        if mean(nums)>23:
            ticket.append(nums)
    return ticket

if __name__=='__main__':
    # print(random_set())
    # print(random_set([1]))
    # print(random_set([2,3,4,5]))

    # print(random_ticket(10))
    # print(random_ticket_each())
    # print(random_ticket_with_neighbout_num(45))

    print(system_ticket(11,5))