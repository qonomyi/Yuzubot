import re


def find_section_by_variable_val(c, val: str):
    # 渡されたvalueが定義されている場所から、連続して定義されている部分を返します。
    # 例: element_typeが書いているソースコードと"physical"が渡された場合、
    # ,g="physical",d="fire",m="ice",~~~
    # のような文字列が返されます。

    # section_pattern = rf'(_\s*,\s*\w+\s*=\s*"{val}".*?r\s*)\)'
    section_pattern = rf',\w+="{val}"(,\w+="\w+")+'
    section_match = re.search(section_pattern, c, re.DOTALL)
    return section_match.group()


def find_alias_map(c):
    # 渡されたコードから、key="value"と書かれている部分を抽出し、
    # {key: value,}のdictとして返します。
    var_defs = {}

    for match in re.finditer(r'(\b\w+)\s*=\s*"([^"]+)"', c):
        var_name, real_value = match.groups()
        var_defs[var_name] = real_value

    return var_defs


def find_id_map_by_two_keys(c, key1: str, key2: str, min_value_length: int = 0):
    # 渡されたコードから、{key: value,}のマッピングを２つのキーを使って探します。
    # 例: key1に201、key2に202を指定した場合
    # {200: v, 201: v, 202: v}のようなデータを探し出します。
    mapping_pattern = (
        r"\{" + key1 + r':"?\w+"?,(\d+:"?\w"?,)+' + key2 + r':"?\w+"?,.+?\}'
    )
    mapping_match = re.search(mapping_pattern, c, re.DOTALL)

    p = re.findall(r"(\w+):(\w+)", mapping_match.group())
    mapping = {k: v for k, v in p}
    return mapping


def find_id_map_by_value(c, key: str, val: str):
    # find_id_map_by_two_keysと同じですが、一つの{key: value}から探します。
    mapping_pattern = r"\{" + f"{key}:{val}" + r",(\w+:\w+,?)+\}"
    mapping_match = re.search(mapping_pattern, c, re.DOTALL)

    p = re.findall(r"(\w+):(\w+)", mapping_match.group())
    mapping = {k: v for k, v in p}
    return mapping


# section = find_section_by_variable_val(js_content, "physical")
# alias_map = find_alias_map(section)
# r_alias_map = {v: k for k, v in alias_map.items()}
# print("alias_map:", alias_map)
#
#
# element_id_map = find_id_map_by_value(js_content, "200", r_alias_map["physical"])
# print("element_id_map:", element_id_map)
#
# sub_element_id_map = find_id_map_by_value(js_content, "1", r_alias_map["frost"])
# print("sub_element_id_map:", sub_element_id_map)
#
# elements = {}
# for k, v in element_id_map.items():
#     elements[k] = alias_map[v]
#
# sub_elements = {}
# for k, v in sub_element_id_map.items():
#     sub_elements[k] = alias_map[v]
#
# print()
# pprint(elements)
# pprint(sub_elements)
