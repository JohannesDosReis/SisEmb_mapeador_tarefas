import json

import numpy as np
from tabulate import tabulate


def read_json_file(filename):
    """
    Faz a leitura de um arquivo json
    :param filename: string nome do arquivo a ser lido
    :returns: json object do arquivo
    """
    with open(filename) as file:
        data = json.load(file)
    return data


def generate_tasks_list(tests_list, apps_list):
    """
    Lista testes contendo lista de tarefas.
    :param tests_list: Lista de testes
    :param apps_list: Lista de apps
    :returns: Lista de testes contendo lista de tarefas
    """
    tasks_lists = []
    index = 0
    for test in tests_list:
        index += 1
        # Informações de cada teste
        tasks_test = {"id": test["id"], "mpsoc_x": test["mpsoc_x"], "mpsoc_y": test["mpsoc_y"],
                      "cluster_x": test["cluster_x"], "cluster_y": test["cluster_y"],
                      "tasks_per_pe": test["tasks_per_pe"], "total_load": 0, "tasks": []}
        for app_qtd in test["apps"]:
            # Encontra o app do teste
            app = list(filter(lambda x: x["name"] == app_qtd["app_name"], apps_list))[0]
            # Adiciona as tarefas
            # print(app_qtd["qtd_apps"])
            for task in app["tasks"]:
                # Adiciona a quantidade apps por teste
                for n in range(app_qtd["qtd_apps"]):
                    task["app_name"] = app["name"] + '_' + str(n)
                    tasks_test["tasks"].append(task.copy())
                    tasks_test["total_load"] += task["load"]

        if (index == 1):
            print(tasks_test['tasks'])
        tasks_lists.append(tasks_test)

    print('\n\n\n\n')
    print(tasks_lists[0]['tasks'])
    input()
    return tasks_lists


def sorted_tasks_table(tasks_lists):
    """
       Ordena ascendentemente as cargas de cada lista de tarefas cargas cada teste.
       :param tasks_lists: Lista de testes contendo lista de tarefas.
       """
    for test in tasks_lists:
        test["tasks"].sort(key=lambda t: t["load"], reverse=True)


def distribute_tasks(tasks_lists):
    """
    Distribui tarefas no mpsoc.
    :param tasks_lists: Lista testes com suas tarefas
    :returns: lista com as tabelas mpsoc
    """
    tests_list = []
    full_result = []
    for test in tasks_lists:
        index = 0
        table = []

        if test["tasks_per_pe"] <= 0:
            print("Sem espaço suficiente no mpsoc para adicionar mais tarefas")
            break

        # Distribui cargas inserindo uma em cada cluster
        # print('\n\n\n\n')
        # print(test)
        for i in range(test["mpsoc_y"] * test["mpsoc_x"]):
            cluster = {"tasks": "", "app": [], "total_load": 0, "len_tasks": 0}
            if index < len(test["tasks"]):
                cluster["tasks"] += "T{}".format(index)
                cluster["total_load"] += test["tasks"][index]["load"]
                cluster["len_tasks"] += 1
                app = {"id": test["tasks"][index]["id"], "name": test["tasks"][index]["app_name"]}
                cluster["app"].append(app)
                # print(test["tasks"][index]["app_name"])
                index += 1
            table.append(cluster)

        # Insere o restante das tarefas sempre no local com cluster com menor carga
        while index < len(test["tasks"]):
            # filtra os cluster disponiveis baseado no numero maximo de tasks_per_pe
            t_filtered = list(
                filter(lambda m: m["len_tasks"] < test["tasks_per_pe"], table))

            min_load = min(t_filtered, key=lambda x: x["total_load"])
            if len(min_load) <= 0:
                print("Sem espaço suficiente no mpsoc para adicionar mais tarefas")
                break
            min_load["tasks"] += " T{}".format(index)
            min_load["total_load"] += test["tasks"][index]["load"]
            min_load["len_tasks"] += 1
            index += 1

        result = (list(map(lambda x: "Tarefas " + x["tasks"] + "\n" + "Carga: " + str(x["total_load"]), table)))
        r = np.array(table).reshape(test["mpsoc_y"], test["mpsoc_x"])
        t = np.array(result, str).reshape(test["mpsoc_y"], test["mpsoc_x"])
        tests_list.append(t)
        full_result.append(r)
    return tests_list, full_result


def show_tables(mpsoc_list):
    """
       Mostra as tabelas de cada mpsoc dos testes.
       :param mpsoc_list: Lista de tabela mpsoc.
       """
    for i, mpsoc in enumerate(mpsoc_list):
        print("Teste " + str(i))
        print(tabulate(mpsoc, tablefmt="fancy_grid"))


def show_tables_step(mpsoc_list):
    """
       Mostra as tabelas de cada mpsoc dos testes.
       :param mpsoc_list: Lista de tabela mpsoc.
       """

    for i, mpsoc in enumerate(mpsoc_list):
        print(tabulate(mpsoc, tablefmt="fancy_grid"))


def messages_total_cost(mpsoc_list, messages_list):
    for i, mpsoc in enumerate(mpsoc_list):
        print(mpsoc)
    # print(messages_list)


def distribute_tasks_step(tasks_lists, indice):
    """
    Distribui tarefas no mpsoc.
    :param tasks_lists: Lista testes com suas tarefas
    :returns: lista com as tabelas mpsoc
    """
    tests_list = []
    test = tasks_lists[indice]
    index = 0
    table = []
    # Distribui cargas inserindo uma em cada cluster
    for i in range(test["mpsoc_y"] * test["mpsoc_x"]):
        cluster = {"tasks": "", "total_load": 0, "len_tasks": 0}
        table.append(cluster)

    for i in range(len(test["tasks"])):
        print(test["tasks"][i]["load"])

    result = (list(map(lambda x: "Tarefas " + x["tasks"] + "\n" + "Carga: " + str(x["total_load"]), table)))
    t = np.array(result, str).reshape(test["mpsoc_y"], test["mpsoc_x"])
    tests_list.append(t)
    show_tables_step(tests_list)

    for i in range(test["mpsoc_y"] * test["mpsoc_x"]):

        if test["tasks_per_pe"] <= 0:
            print("Sem espaço suficiente no mpsoc para adicionar mais tarefas")
            break

        cluster = {"tasks": "", "total_load": 0, "len_tasks": 0}
        if index < len(test["tasks"]):
            cluster["tasks"] += "T{}".format(index)
            cluster["total_load"] += test["tasks"][index]["load"]
            cluster["len_tasks"] += 1
            index += 1
        else:
            break
        input('')
        table[i] = cluster
        for j in range(index, len(test["tasks"])):
            print(test["tasks"][j]["load"])
        result = (list(map(lambda x: "Tarefas " + x["tasks"] + "\n" + "Carga: " + str(x["total_load"]), table)))
        t = np.array(result, str).reshape(test["mpsoc_y"], test["mpsoc_x"])
        tests_list[0] = t
        show_tables_step(tests_list)

    # Insere o restante das tarefas sempre no local com cluster com menor carga
    while index < len(test["tasks"]):
        # filtra os cluster disponiveis baseado no numero maximo de tasks_per_pe
        t_filtered = list(
            filter(lambda m: m["len_tasks"] < test["tasks_per_pe"], table))

        min_load = min(t_filtered, key=lambda x: x["total_load"])
        if len(min_load) <= 0:
            print("Sem espaço suficiente no mpsoc para adicionar mais tarefas")
            break
        min_load["tasks"] += " T{}".format(index)
        min_load["total_load"] += test["tasks"][index]["load"]
        min_load["len_tasks"] += 1
        index += 1
        input('')
        for i in range(index, len(test["tasks"])):
            print(test["tasks"][i]["load"])
        result = (list(map(lambda x: "Tarefas " + x["tasks"] + "\n" + "Carga: " + str(x["total_load"]), table)))
        t = np.array(result, str).reshape(test["mpsoc_y"], test["mpsoc_x"])
        tests_list[0] = t
        show_tables_step(tests_list)

    return tests_list


if __name__ == '__main__':

    while (True):
        versao = int(input('Selecione o tipo: Direto - 1 , Passo a Passo - 2\n'))
        if (versao == 1):
            # Leitura arquivo de testes
            tests = read_json_file("tests.json")
            # Leitura arquivo de apps
            apps_tests = read_json_file("apps_test.json")
            # Leitura do arquivo de mensagens
            messages = read_json_file("messages.json")
            # Gera lista de testes contendo cada uma uma lista de tarefas
            tasks_table = generate_tasks_list(tests, apps_tests)
            # Ordena as lista de tarefas de cada teste de forma ascendente
            sorted_tasks_table(tasks_table)
            # Distribiu as tarefas em uma tabela representando o mpsoc
            mpsocs, full_mpsocs = distribute_tasks(tasks_table)
            # Mostra a tabela de mpsoc
            show_tables(mpsocs)
            # Calcula mensagens
            full_tasks_table = messages_total_cost(full_mpsocs, messages)

            break
        elif (versao == 2):
            indice = int(input('Selecione o teste\n'))
            # Leitura arquivo de testes
            tests = read_json_file("tests.json")
            # Leitura arquivo de apps
            apps_tests = read_json_file("apps_test.json")
            # Gera lista de testes contendo cada uma uma lista de tarefas
            tasks_table = generate_tasks_list(tests, apps_tests)
            # Ordena as lista de tarefas de cada teste de forma ascendente
            sorted_tasks_table(tasks_table)
            # Distribiu as tarefas em uma tabela representando o mpsoc
            mpsocs = distribute_tasks_step(tasks_table, indice)
            break
