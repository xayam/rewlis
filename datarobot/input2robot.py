import json
import os.path

input_rus = "input_rus.txt"
input_eng = "input_eng.txt"


def read(filename):
    with open(filename, mode="r", encoding="UTF-8") as f:
        return f.readlines()


def get_id_name(data):
    buffer = data.strip().split(" ")
    ids = buffer[0].encode().decode()
    name = " ".join(buffer[1:]).encode().decode()
    return ids, name


def main():
    list_rus = read(input_rus)
    list_eng = read(input_eng)
    dict_result = {}
    for index in range(len(list_rus)):
        id_rus, name_rus = get_id_name(list_rus[index])
        id_eng, name_eng = get_id_name(list_eng[index])
        if id_rus == id_eng:
            key = f"input/{id_rus}.htm"
            if not os.path.exists(key):
                continue
            dict_result[key] = {}
            dict_result[key]["rus"] = name_rus
            dict_result[key]["eng"] = name_eng

    with open("robot.json", mode="w", encoding="utf-8") as f:
        json.dump(dict_result, f)

    return dict_result


if __name__ == "__main__":
    result = main()
    print(result)
    print(len(result))
