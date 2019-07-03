from statistics import mean, pstdev

def random_select_rule():
    return {
        "description": "random select",
        "condition": lambda nums : True,
        "prefill": []
    }

def rules():
    rules = [
    {
        "description": "2 neighbour numbers",
        "condition": lambda nums : len(set([num+1 for num in nums]) & set(nums))>0,
        "prefill": []
    },
    {
        "description": "lower average",
        "condition": lambda nums : mean(nums)<23,
        "prefill": []
    },
    {
        "description": "higher average",
        "condition": lambda nums : mean(nums)>23,
        "prefill": []
    }
    ]

    for i in range(1, 46):
        rules.append(rules_with_specified_num(i))
    
    return rules

def rules_with_specified_num(num):
    return {
        "description": "has "+str(num),
        "condition": lambda nums : True,
        "prefill": [num]
    }