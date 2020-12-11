import sys
from psd_tools import PSDImage


def print_child(layer, origin):
    if layer.kind == "type":
        text = str(layer.engine_dict['Editor']['Text']).strip("'")
        font_index = layer.resource_dict["StyleSheetSet"][0]["StyleSheetData"]["Font"]
        font_name = layer.resource_dict["FontSet"][font_index]["Name"]
        font_name = str(font_name).strip("'")
        font_size = layer.resource_dict["StyleSheetSet"][0]["StyleSheetData"]["FontSize"]
    
    return f'{{\n' + \
    f'"name": "{layer.name}",\n' + \
    (f'"text": "{text}",\n' + \
    f'"font": "{font_name}",\n' + \
    f'"font_size": "{font_size}",\n' \
        if hasattr(layer, "text") else '') + \
    f'"width": "{layer.width}",\n' +  \
    f'"height": "{layer.height}",\n' +  \
    f'"top": "{layer.left - origin[0]}",\n' + \
    f'"left": "{layer.top - origin[1]}"\n}}'

def print_group(layer, child, origin):
    return f'{{\n' + \
    f'"name": "{layer.name}",\n' + \
    f'"width": "{layer.width}",\n' +  \
    f'"height": "{layer.height}",\n' +  \
    f'"top": "{layer.left - origin[0]}",\n' + \
    f'"left": "{layer.top - origin[1]}",\n' + \
    f'"child": [\n{child}\n]\n}}'

def tree_search(layer, origin=(0,0)):
    if layer.is_group():
        if origin == (0, 0):
            origin = (layer.left, layer.top)
        child_list = [tree_search(child, origin) for child in layer]
        return print_group(layer, ',\n'.join(child_list), origin)
    else:
        return print_child(layer, origin)

def print_list(list):
    return ',\n'.join(list)

def build_tree(psd):
    layer_list = [tree_search(layer) for layer in psd]
    return f'{{\n"layers": [\n{print_list(layer_list)}\n]}}'

def main():
    args = sys.argv[1:]
    input = args[0]
    output = args[1]

    psd = PSDImage.open(input)

    with open(output, 'w') as w:
        w.write(build_tree(psd))

main()