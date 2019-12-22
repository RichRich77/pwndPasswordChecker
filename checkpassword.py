import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    # password: testtest123 = 6D74062482BE7F3F06BF0D5DF5DED5C7B5AE600E  https://passwordsgenerator.net/sha1-hash-generator/
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error Fetching: {res.status_code}, Check the API')
    return res

def get_passwords_breached_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        #print(h, count)'
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5char)
    # print(first5char,tail, response)
    return get_passwords_breached_count(response, tail)

# pwned_api_check('loveamericanstyle')

# Original main() function being called using sys.argv[1:]
# def main(args):
#     for password in args:
#         count = pwned_api_check(password)
#         if count:
#             print(f'{password} was found {count} times. Be sure to change your password!')
#         else:
#             print(f'{password} was NOT found.')
#     return 'Check Completed'


def main():
    password = input('Type a Password: ')
    # for password in args:
    count = pwned_api_check(password)
    if count:
        print(f'{password} was found {count} times. Be sure to change your password!')
    else:
        print(f'{password} was NOT found.')
    return 'Check Completed'


if __name__ == '__main__':
    sys.exit(main())
    # sys.exit(main(sys.argv[1:]))
