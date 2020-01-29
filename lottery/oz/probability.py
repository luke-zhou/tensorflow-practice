import oz_generator as generator
import oz_verify as verifier
import json
from statistics import mean, pstdev
from math import factorial 

def calculate(generator_type, ticket_size, sample_size):
    draw = generator.random_draw()
    print(draw)

    if generator_type =='simple':
        generator_method = generator.random_ticket
        method_args=[]
    elif 'system' in generator_type:
        generator_method = generator.system_ticket
        method_args=[int(generator_type[6:])]
        
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
    result['total_jackpot'] = sum([x['jackpot_count'] for x in all_sample_results])
    result['jackpot_rate'] = result['total_jackpot']/sample_size
    result['samples_with_jackpot'] = len([x for x in all_sample_results if x['jackpot_count']>0])
    result['samples_with_jackpot_rate'] = result['samples_with_jackpot']/sample_size

    return result

if __name__ =='__main__':
    f7=factorial(7)
    sample_size=5000
    # print('each system ticket compare with same size of normal ticket')
    # for i in range(8, 21):
    #     ticket_size = int(factorial(i)/(f7*factorial(i-7)))
    #     print('system'+str(i)+': '+str(ticket_size))
    #     print('normal ticket:')
    #     result = calculate('simple', ticket_size, sample_size)
    #     print(result['average_prize'])
    #     print(result['pstd_prize'])
    #     print(result['highest_division']) 
    #     print('system ticket:')
    #     result = calculate('system'+str(i), 1, sample_size)
    #     print(result['average_prize'])
    #     print(result['pstd_prize'])
    #     print(result['highest_division'])

    # print('system ticket compare with each other in the same size ')
    # ticket_size = int(factorial(20)/(f7*factorial(20-7)))*10
    # for i in range(8, 21):
    #     current_ticket_size = int(factorial(i)/(f7*factorial(i-7)))
    #     actual_ticket_size = int(ticket_size/current_ticket_size)
    #     print('system'+str(i)+': '+str(actual_ticket_size))
    #     print('system ticket:')
    #     result = calculate('system'+str(i), actual_ticket_size, sample_size)
    #     print(result['average_prize'])
    #     print(result['pstd_prize'])
    #     print(result['highest_division'])

    # print('normal ticket: '+str(ticket_size))
    # result = calculate('simple', ticket_size, sample_size)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division']) 

    print('compare different ticket size of the same system ticket')
    for i in range(10, 101, 10):
        print('system:' +str(i))
        print('system ticket:')
        result = calculate('system8', i, sample_size)
        print(result['average_prize'])
        print(result['pstd_prize'])
        print(result['highest_division'])
        print(result['total_jackpot'])
        print(result['jackpot_rate'])
        print(result['samples_with_jackpot'])
        print(result['samples_with_jackpot_rate'])


    # result = calculate('simple', 400, 20)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division'])

    # result = calculate('system8', 50, 20)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division'])

    # result = calculate('simple', 360, 20)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division'])

    # result = calculate('system9', 10, 20)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division'])

    # result = calculate('simple', 360, 20)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division'])

    # result = calculate('system10', 3, 20)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division'])

    # result = calculate('simple', 330, 20)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division'])

    # result = calculate('system11', 1, 20)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division'])

    # result = calculate('simple', 792, 20)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division'])

    # result = calculate('system12', 1, 20)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division'])

    # result = calculate('simple', 1716, 20)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division'])

    # result = calculate('system13', 1, 20)
    # print(result['average_prize'])
    # print(result['pstd_prize'])
    # print(result['highest_division'])

