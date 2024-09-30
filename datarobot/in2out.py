import os.path
from bs4 import BeautifulSoup

input_rus = "input_rus.txt"
input_eng = "input_eng.txt"


def read(filename):
    with open(filename, mode="r", encoding="UTF-8") as f:
        return f.readlines()


def get_id_name(data):
    buffer = data.strip().split(" ")
    ids = buffer[0]
    name = " ".join(buffer[1:])
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
            with open(key, mode="r", encoding="windows-1251") as f:
                html_text = f.read()
            soup = BeautifulSoup(html_text, "html.parser")
            name_rus = soup.select('h1')[0].text.strip()
            name_rus = name_rus.encode(encoding="windows-1251"). \
                decode(encoding="utf-8")
            dict_result[key] = {}
            dict_result[key]["rus"] = name_rus
            dict_result[key]["eng"] = name_eng
    return dict_result


if __name__ == "__main__":
    result = main()
    print(result)
    print(len(result))
