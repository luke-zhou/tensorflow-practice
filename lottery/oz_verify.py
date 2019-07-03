import oz_generator as generator
from statistics import mean, pstdev

def verify_set(original_set, new_set):
    result = set(original_set) & set(new_set)
    return {'match_nums':list(result), 'match_count':len(result)}

def verify_ticket(original_set, ticket):
    result = {'results':[verify_set(original_set, new_set) for new_set in ticket]}
    match_count_lst=[result['match_count'] for result in result['results']]
    result['average_match_count'] =mean(match_count_lst)
    result['pstd_match_count'] =pstdev(match_count_lst)
    return result

if __name__ == '__main__':
    original_set=[1,2,3,4,5,6,7]
    print(mean(original_set))
    print(pstdev(original_set))
    new_set=[2,3,4,5,6,7,8]
    print(verify_set(original_set, new_set)) 

    new_ticket = generator.random_ticket_each()
    print(verify_ticket(original_set, new_ticket))

    new_ticket = generator.random_ticket(45)
    print(verify_ticket(original_set, new_ticket))