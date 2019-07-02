import random
import time

def random_gen(prefill =[] ):
    millis = int(round(time.time() * 1000))
    random.seed(a = millis)
    result = set(prefill)
    while len(result) < 7:
        num = random.randint(1, 45)
        result.add(num)
    
    return sorted(list(result))

if __name__=='__main__':
    print(random_gen())
    print(random_gen([1]))
    print(random_gen([2,3,4,5]))