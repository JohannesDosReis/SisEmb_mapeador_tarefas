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
    for test in tests_list:
        # Informações de cada teste
        tasks_test = {"id": test["id"], "mpsoc_x": test["mpsoc_x"], "mpsoc_y": test["mpsoc_y"],
                      "cluster_x": test["cluster_x"], "cluster_y": test["cluster_y"],
                      "tasks_per_pe": test["tasks_per_pe"], "total_load": 0, "tasks": []}

        for app_qtd in test["apps"]:
            # Encontra o app do teste
            app = list(filter(lambda x: x["name"] == app_qtd["app_name"], apps_list))[0]
            # Adiciona as tarefas
            for task in app["tasks"]:
                # Adiciona a quantidade apps por teste
                for n in range(app_qtd["qtd_apps"]):
                    task["app_name"] = app["name"]
                    tasks_test["tasks"].append(task)
                    tasks_test["total_load"] += task["load"]
        tasks_lists.append(tasks_test)
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
    for test in tasks_lists:
        index = 0
        table = []

        if test["tasks_per_pe"] <= 0:
            print("Sem espaço suficiente no mpsoc para adicionar mais tarefas")
            break

        # Distribui cargas inserindo uma em cada mpsoc
        for i in range(test["mpsoc_y"] * test["mpsoc_x"]):
            mp = {"tasks": "", "total_load": 0, "len_tasks": 0}
            if index < len(test["tasks"]):
                mp["tasks"] += "T{}".format(index)
                mp["total_load"] += test["tasks"][index]["load"]
                mp["len_tasks"] += 1
                index += 1
            table.append(mp)

        # Insere o restante das tarefas sempre no local com cluster com menor carga
        while index < len(test["tasks"]):
            # filtra os cluster disponiveis baseado no numero maximo de tasks_per_pe
            t_filtered = list(
                filter(lambda m: m["len_tasks"] < test["mpsoc_y"] * test["mpsoc_x"] * test["tasks_per_pe"], table))

            min_load = min(t_filtered, key=lambda x: x["total_load"])
            if len(min_load) <= 0:
                print("Sem espaço suficiente no mpsoc para adicionar mais tarefas")
                break
            min_load["tasks"] += " T{}".format(index)
            min_load["total_load"] += test["tasks"][index]["load"]
            min_load["len_tasks"] += 1
            index += 1

        result = (list(map(lambda x: "Tarefas " + x["tasks"] + "\n" + "Carga: " + str(x["total_load"]), table)))
        t = np.array(result, str).reshape(test["mpsoc_y"], test["mpsoc_x"])
        tests_list.append(t)
    return tests_list


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
    # Distribui cargas inserindo uma em cada mpsoc
    for i in range(test["mpsoc_y"] * test["mpsoc_x"]):
        mp = {"tasks": "", "total_load": 0, "len_tasks": 0}
        table.append(mp)

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

        mp = {"tasks": "", "total_load": 0, "len_tasks": 0}
        if index < len(test["tasks"]):
            mp["tasks"] += "T{}".format(index)
            mp["total_load"] += test["tasks"][index]["load"]
            mp["len_tasks"] += 1
            index += 1
        else:
            break
        input('')
        table[i] = mp
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
            filter(lambda m: m["len_tasks"] < test["mpsoc_y"] * test["mpsoc_x"] * test["tasks_per_pe"], table))

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
            # Gera lista de testes contendo cada uma uma lista de tarefas
            tasks_table = generate_tasks_list(tests, apps_tests)
            # Ordena as lista de tarefas de cada teste de forma ascendente
            sorted_tasks_table(tasks_table)
            # Distribiu as tarefas em uma tabela representando o mpsoc
            mpsocs = distribute_tasks(tasks_table)
            # Mostra a tabela de mpsoc
            show_tables(mpsocs)
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
