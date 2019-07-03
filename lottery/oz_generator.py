import random
import time
from statistics import mean, pstdev

millis = int(round(time.time() * 1000))
random.seed(a = millis)

def random_set(prefill =[]):
    result = set(prefill)
    while len(result) < 7:
        num = random.randint(1, 45)
        result.add(num)
    
    return sorted(list(result))

def generate_ticket(size, conditions, prefill=[]):
    ticket =[]
    time_out = 1000
    while len(ticket) < size and time_out>0:
        nums = random_set(prefill)
        condition_results = [condition(nums) for condition in conditions]
        if all(condition_results):
            ticket.append(nums)
        time_out-=1
        # print(time_out)
    return ticket

def random_ticket(size):
    return [random_set() for i in range(size)]

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
    print(random_ticket_with_neighbout_num(45))