from jsparser import *

section = find_section_by_variable_val(js_content, "physical")
alias_map = find_alias_map(section)
r_alias_map = {v: k for k, v in alias_map.items()}
print("alias_map:", alias_map)


element_id_map = find_id_map_by_value(js_content, "200", r_alias_map["physical"])
print("element_id_map:", element_id_map)

sub_element_id_map = find_id_map_by_value(js_content, "1", r_alias_map["frost"])
print("sub_element_id_map:", sub_element_id_map)

elements = {}
for k, v in element_id_map.items():
    elements[k] = alias_map[v]

sub_elements = {}
for k, v in sub_element_id_map.items():
    sub_elements[k] = alias_map[v]

print()
