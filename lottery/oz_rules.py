from statistics import mean, pstdev
import oz_generator as generator

def random_select_rule():
    return {
        "description": "random select",
        "condition": lambda nums : True,
        "prefill": []
    }

def impossible_combine():
    combine = [
        ("lower average", "higher average"),
        ("2 neighbour numbers", "all odd"),
        ("2 neighbour numbers", "all even"),
        ("all odd", "all even"),
        ("all odd", "3 neighbour numbers"),
        ("all even", "3 neighbour numbers")
    ]

    for i in range(1, 46, 2):
        combine.append(("all even", "has "+str(i)))
    
    for i in range(2, 46, 2):
        combine.append(("all odd", "has "+str(i)))

    for rule in existing_rules():
        combine.append((rule['description'], rule['description']))
    
    return combine
def new_rules():
    return [
        {
            "description": "3 neighbour numbers",
            "condition": lambda nums : len(set([num+2 for num in nums]) & set([num+1 for num in nums]) & set(nums))>0,
            "prefill": []
        },
        {
            "description": "neighbour numbers gap 2",
            "condition": lambda nums : len(set([num+2 for num in nums]) & set(nums))>0,
            "prefill": []
        },
        {
            "description": "three in 10",
            "condition": lambda nums : len([num for num in nums if num <10])>=3,
            "prefill": []
        },
        {
            "description": "three in 20",
            "condition": lambda nums : len([num for num in nums if num <20 and num >=10])>=3,
            "prefill": []
        },
        {
            "description": "three in 30",
            "condition": lambda nums : len([num for num in nums if num <30 and num >=20])>=3,
            "prefill": []
        },
        {
            "description": "three in 40",
            "condition": lambda nums : len([num for num in nums if num <40 and num >=30])>=3,
            "prefill": []
        },
        {
            "description": "three in 50",
            "condition": lambda nums : len([num for num in nums if num <50 and num >=40])>=3,
            "prefill": []
        }
    ]

def existing_rules():
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
    },
    {
        "description": "all odd",
        "condition": lambda nums : all([num%2==1 for num in nums]),
        "prefill": []
    },
    {
        "description": "all even",
        "condition": lambda nums : all([num%2==0 for num in nums]),
        "prefill": []
    },
    {
        "description": "3 neighbour numbers",
        "condition": lambda nums : len(set([num+2 for num in nums]) & set([num+1 for num in nums]) & set(nums))>0,
        "prefill": []
    },
    {
        "description": "neighbour numbers gap 2",
        "condition": lambda nums : len(set([num+2 for num in nums]) & set(nums))>0,
        "prefill": []
    },
    {
        "description": "three in 10",
        "condition": lambda nums : len([num for num in nums if num <10])>=3,
        "prefill": []
    },
    {
        "description": "three in 20",
        "condition": lambda nums : len([num for num in nums if num <20 and num >=10])>=3,
        "prefill": []
    },
    {
        "description": "three in 30",
        "condition": lambda nums : len([num for num in nums if num <30 and num >=20])>=3,
        "prefill": []
    },
    {
        "description": "three in 40",
        "condition": lambda nums : len([num for num in nums if num <40 and num >=30])>=3,
        "prefill": []
    },
    {
        "description": "three in 50",
        "condition": lambda nums : len([num for num in nums if num <50 and num >=40])>=3,
        "prefill": []
    }
    ]

    for i in range(1, 46):
        rules.append(rules_with_specified_num(i))
    
    return rules

def rules_with_specified_num(num):
    return {
        "description": "has "+str(num),
        "condition": lambda nums : num in nums,
        "prefill": [num]
    }

def verify_rule(rules):
    conditions = [rule["condition"] for rule in rules]
    prefills = [rule["prefill"] for rule in rules]
    ticket = generator.generate_ticket(45, conditions , prefills)
    print(ticket)

if __name__=='__main__':

    verify_rule([new_rules()[0], existing_rules()[0]])
    # print(impossible_combine())