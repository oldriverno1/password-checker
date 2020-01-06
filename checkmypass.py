import hashlib
import sys
import requests


def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"status code: {res.status_code}, check again!")
    return res


def send_encrypted_password(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_leaks_count(response, tail)


def get_leaks_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def main(args):
    for password in args:
        count = send_encrypted_password(password)
        if count:
            print(f"{password} was found {count} times, better use a new one!")
        else:
            print(f"{password} is good to go!")


if __name__ == "__main__":
    main(sys.argv[1:])
