from random import choice

def get_random_letters(number):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return "".join([choice(letters) for i in range(number)])

def generate_code(collector):
    code_num = collector.code_set.all().count()
    code_num += 1

    cfn = "%d-%d" %(collector.id, code_num)
    ecn = get_random_letters(1)

    return cfn, ecn
