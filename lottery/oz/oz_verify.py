import oz_generator as generator
from statistics import mean, pstdev
import json

divisions={
    (3, True):(7,1),
    (4, True):(6,2),
    (4, False):(6,2),
    (5, False):(5,4),
    (5, True):(4,30),
    (6, False):(3,400),
    (6, True):(2,2000),
    (7, False):(1,200000)
}

def verify_nums(draw, nums):
    match_nums = set(draw['nums']) & set(nums)
    match_supps = set(draw['supps']) & set(nums)
    division_details = divisions.get((len(match_nums), len(match_supps)>0), (None, 0))
    return {
        'match_nums':list(match_nums), 
        'match_supps':list(match_supps), 
        'division': division_details[0],
        'prize': division_details[1] 
        }

def convert_system_set_to_normal(s):
    normal_nums=[]
    for i in range(len(s)):
        for j in range(i+1, len(s)):
            for k in range(j+1, len(s)):
                for l in range(k+1, len(s)):
                    for m in range(l+1, len(s)):
                        for n in range(m+1, len(s)):
                            for o in range(n+1, len(s)):
                                normal_nums.append([s[i],s[j], s[k], s[l], s[m], s[n],s[o]])
    
    return normal_nums

def convert_all_sets_to_nornmal(ticket):
    new_ticket = []
    for x in ticket:
        if len(x) ==7:
            new_ticket.append(x)
        elif len(x) >7:
            new_ticket.extend(convert_system_set_to_normal(x))
    
    return new_ticket      

def verify_ticket(draw, ticket):
    result = {'details':[verify_nums(draw, nums) for nums in ticket]}
    total_prize = sum([result['prize'] for result in result['details']])
    result['total_prize']=total_prize
    divisions = [result['division'] for result in result['details'] if result['division'] is not None]
    highest_division = min(divisions) if divisions else None
    result['highest_division'] =highest_division
    # match_count_lst=[result['match_count'] for result in result['results']]
    # result['average_match_count'] =mean(match_count_lst)
    # result['pstd_match_count'] =pstdev(match_count_lst)
    # win_match = [match for match in match_count_lst if match >2]
    # result['win_match']=win_match
    # result['win_time']=len(win_match)
    # result['win_price']= sum([2**(match-3) for match in win_match])
    return result    

if __name__ == '__main__':
    # original_set=[1,2,3,4,5,6,7]
    # print(mean(original_set))
    # print(pstdev(original_set))
    # new_set=[2,3,4,5,6,7,8]
    # print(verify_set(original_set, new_set)) 

    # new_ticket = generator.random_ticket_each()
    # print(verify_ticket(original_set, new_ticket))

    # new_ticket = generator.random_ticket(45)
    # print(verify_ticket(original_set, new_ticket))

    draw = generator.random_draw()
    print(draw)
    # nums = generator.random_set()
    # print(nums)
    # print(verify_nums(draw, nums))

    # new_ticket = generator.random_ticket(20)
    # print(new_ticket)
    # result = verify_ticket(draw, new_ticket)
    # win_result =[ x for x in result['details'] if x['prize']>0]
    # print(json.dumps(win_result, indent=4))
    # print(result['total_prize'])
    # print(result['highest_division'])

    # system_set=[1,2,3,4,5,6,7, 8, 9]
    # result = convert_system_set_to_normal(system_set)
    # print(result)
    # print(len(result))

    ticket = generator.system_ticket(9, 50)
    print(ticket)
    result = verify_ticket(draw, ticket)
    win_result =[ x for x in result['details'] if x['prize']>0]
    print(json.dumps(win_result, indent=4))
    print(result['total_prize'])
    print(result['highest_division'])