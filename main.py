import json


# Faz a leitura do arquivo de testes.
def read_tests_json():
    with open("tests.json") as tests_json:
        global tests
        tests = json.load(tests_json)
        # print(json.dumps(tests, indent=4))


# Faz a leitura do arquivo de apps para os testes.
def read_apps_tests_json():
    with open("apps_test.json") as apps_tests_json:
        global apps_tests
        apps_tests = json.load(apps_tests_json)
        # print(json.dumps(apps_tests, indent=4))


def generate_tasks_list():
    global tasks_lists, tests, apps_tests
    for t, test in enumerate(tests):
        # print("Test ", t)
        tasks = []
        for app_qtd in test["apps"]:
            # print("App qtd", app_qtd)
            app = list(filter(lambda x: x["name"] == app_qtd["app_name"], apps_tests))[0]
            # print("app", app)
            # print()
            for task in app["tasks"]:
                for n in range(app_qtd["qtd_apps"]):
                    tasks.append(task)
        # print(tasks)
        tasks_lists.append(tasks)
        # print()


def sorted_tasks_list():
    global tasks_lists
    for tasks in tasks_lists:
        tasks.sort(key=lambda t: t["load"], reverse=True)
        # print(tasks)


tests = []
apps_tests = []
tasks_lists = []

if __name__ == '__main__':
    read_tests_json()
    read_apps_tests_json()
    generate_tasks_list()
    # print(tasks_lists)
    sorted_tasks_list()

    print()
    # for task_list in tasks_lists:
    #     for task in task_list:
    # print(task)
    # print(tasks_lists)
