import oz_generator as generator
import oz_verify as verifier
import json
from statistics import mean, pstdev

def calculate(generator_type, ticket_size, sample_size):
    draw = generator.random_draw()
    print(draw)

    if generator_type =='simple':
        generator_method = generator.random_ticket
        method_args=[]
    elif generator_type=='system8':
        generator_method = generator.system_ticket
        method_args=[8]
    elif generator_type=='system9':
        generator_method = generator.system_ticket
        method_args=[9]
        
    all_sample_results = []
    for _ in range(sample_size):
        ticket = generator_method(*method_args, ticket_size)
        result = verifier.verify_ticket(draw, ticket)
        all_sample_results.append(result)
        # win_result =[ x for x in result['details'] if x['prize']>0]
        # print(json.dumps(win_result, indent=4))
        # print(result['total_prize'])
        # print(result['highest_division'])
    result={'details':all_sample_results}
    total_prizes = [x['total_prize'] for x in all_sample_results]
    divisions = [x['highest_division'] for x in all_sample_results if x['highest_division'] is not None]
    result['average_prize'] = mean(total_prizes)
    result['pstd_prize'] = pstdev(total_prizes)
    result['highest_division'] = min(divisions) if divisions else None
    return result

if __name__ =='__main__':
    result = calculate('simple', 400, 20)
    print(result['average_prize'])
    print(result['pstd_prize'])
    print(result['highest_division'])

    result = calculate('system8', 50, 20)
    print(result['average_prize'])
    print(result['pstd_prize'])
    print(result['highest_division'])

    result = calculate('simple', 360, 20)
    print(result['average_prize'])
    print(result['pstd_prize'])
    print(result['highest_division'])

    result = calculate('system9', 10, 20)
    print(result['average_prize'])
    print(result['pstd_prize'])
    print(result['highest_division'])

