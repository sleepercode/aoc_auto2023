import requests
import datetime
import json
import time
from subprocess import Popen, PIPE, STDOUT


def get_input(p_dan, p_session):
    cookies = {
        'session': p_session,
    }

    headers = {
        # 'Cookie': 'cookie_name=cookie_value',
    }
    #dan = datetime.datetime.today().day
    status_code = 404
    while status_code == 404:
        response = requests.get(f"https://adventofcode.com/2023/day/{p_dan}/input", cookies=cookies, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            file = open(f"{p_dan}.txt", "w")
            file.write(response.text)
            file.close()
            print(f"kreiran fajl input: {p_dan}.txt")
        else:
            status_code = 404
            print('waiting 20 seconds')
            time.sleep(20)

def get_skripta(p_dan):

    status_code = 404
    probaj_skriptu  = 0  # Initialize pokusaj variable
    while status_code == 404:
        response = requests.get(f"https://github.com/jonathanpaulson/AdventOfCode/blob/master/2023/{p_dan}.py")
        status_code = response.status_code
        if status_code == 200:
            probaj_skriptu = 1  # setovanje skripte
            string = response.text
            dict = json.loads(string)
            rawlines = dict['payload']['blob']['rawLines']
            skripta = '\n'.join(rawlines)
            file = open(f"{p_dan}.py", "w")
            file.write(skripta)
            print(f"kreiran fajl skripta1: {p_dan}.py")
            #return probaj_skriptu 
            
        if status_code == 404:
            response = requests.get(f"https://github.com/oliver-ni/advent-of-code/blob/master/py/2023/day{p_dan}.py")
            status_code = response.status_code
            if status_code == 200:
                probaj_skriptu = 2  # setovanje skripte
                string = response.text
                dict = json.loads(string)
                rawlines = dict['payload']['blob']['rawLines']
                skripta = '\n'.join(rawlines)
                file = open(f"{p_dan}.py", "w")
                file.write(skripta)
                print(f"kreiran fajl skripta2: {p_dan}.py")
                #return probaj_skriptu
                
        else:
            status_code = 404
            print('waiting 15 seconds')
            time.sleep(15)
        return probaj_skriptu 
    
def submit_odgovor(p_dan, p_session, p_odgovor1, p_odgovor2):
    cookies = {
        'session': p_session,
    }

    headers = {
    }

    payload = {'level': '1',
               'answer': p_odgovor1}

    payload2 = {'level': '2',
                'answer': p_odgovor2}

    response = requests.post(f"https://adventofcode.com/2023/day/{p_dan}/answer", cookies=cookies, headers=headers, data=payload)

    time.sleep(5)

    response2 = requests.post(f"https://adventofcode.com/2023/day/{p_dan}/answer", cookies=cookies, headers=headers, data=payload2)

def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def run_skripta (cmd):
    #cmd = "python 6.py test_input.txt"
    proc = Popen(cmd.split(' '), stdout=PIPE, stderr=PIPE)
    (output, error) = proc.communicate()
    output=output.decode("utf-8")
    poz1 = output.find('\r\n')
    rez1 = output[:poz1]
    poz2 = find_nth(output,'\r\n',2)
    rez2 = output[poz1+2:poz2]
    print (f"output={output}")
    print (error)
    print(f"rez1={rez1} rez2={rez2}")
    return rez1, rez2


if __name__ == '__main__':
    session = 'your_session_id'
    dan = datetime.datetime.today().day
    #dan = 19
    get_input(dan, session)
    #get_skripta(dan)
    odabrana_skripta = get_skripta(dan)
    print (f"Odabrana skripta: {odabrana_skripta}")


    if odabrana_skripta == 1:
        print (odabrana_skripta)
        print(f"python {dan}.py {dan}.txt")
        p_odgovor1,p_odgovor2 = run_skripta(f"python {dan}.py {dan}.txt")


    if  odabrana_skripta == 2:
        print (odabrana_skripta)
        print(f"python run.py py.2023.day{dan}")
        p_odgovor1,p_odgovor2 = run_skripta(f"python run.py --y 2023 --day {dan}")

    #p_odgovor1 = ''
    #p_odgovor2 = ''
    submit_odgovor(dan, session, p_odgovor1, p_odgovor2)
    print(f"submitano")