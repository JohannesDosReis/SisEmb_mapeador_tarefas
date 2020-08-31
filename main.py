import json


# Faz a leitura do arquivo de testes.
def read_tests_json():
    with open("tests.json") as tests_json:
        global tests
        tests = json.load(tests_json)
        print(json.dumps(tests, indent=4))


# Faz a leitura do arquivo de apps para os testes.
def read_apps_tests_json():
    with open("apps_test.json") as apps_tests_json:
        global tests
        tests = json.load(apps_tests_json)
        print(json.dumps(tests, indent=4))


tests = []
apps_tests = []

if __name__ == '__main__':
    read_tests_json()
    read_apps_tests_json()
