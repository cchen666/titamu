import commands
import time
import random

def loop_check(cmd, interval, retry, result):
    while retry > 0:
        if commands.getoutput(cmd).strip() == result:
            return 0
        else:
            time.sleep(interval)
            retry -= 1
            if retry == 1:
                return 1


def gen_random(number, range_start, range_end):
    result = ""
    for i in range(number):
        result += str(random.randint(range_start, range_end))
    return result
