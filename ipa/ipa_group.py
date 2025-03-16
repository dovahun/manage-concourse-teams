from python_freeipa import Client
import argparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help='path to file')
    parser.add_argument('-u', type=str, help='FreeIPA host')
    parser.add_argument('-l', type=str, help='FreeIPA login')
    parser.add_argument('-p', type=str, help='FreeIPA password')
    argument = vars(parser.parse_args())
    return argument


def connect(ipa_host, ipa_user, ipa_password):
    client = Client(ipa_host, version='2.215', verify_ssl=False)
    client.login(ipa_user, ipa_password)
    return client


def read_file(path):
    with open(path) as file:
        rows = file.readlines()
    return rows


arguments = args()
client = connect(arguments['u'], arguments['l'], arguments['p'])
rows = read_file(arguments['f'])
for row in rows:
    group_name = row.rstrip()
    search_result = client.group_find(group_name)
    if search_result['count'] == 0:
        if client.group_add(group=group_name, description="concourse team {} group".format(group_name)):
            print('created {} group in freeipa'.format(group_name))
