import os

def read_lines(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.rstrip('\n') for line in file]

def write_lines(filename, lines):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')

def split_library_file(input_path, output_dir):
    lines = read_lines(input_path)

    standard_header = [
        "EESchema-LIBRARY Version 2.3",
        "#encoding utf-8",
        "#",
    ]

    standard_footer = [
        "#",
        "#End Library"
    ]

    components = []
    current_component = None
    component_name = None

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("DEF ") and " " in line:
            # 提取元件名称
            component_name = line.split()[1]
            current_component = [
                f"# {component_name}",  # 标题行
                "#"                       # 空行分隔
            ]
            current_component.append(line)
            i += 1
            while i < len(lines):
                next_line = lines[i]
                current_component.append(next_line)
                if next_line.startswith("ENDDEF"):
                    break
                i += 1
            components.append((component_name, current_component))
        else:
            i += 1

    # 写入每个组件
    for name, comp_lines in components:
        full_content = standard_header + comp_lines + standard_footer
        output_path = os.path.join(output_dir, f"{name}.lib")
        write_lines(output_path, full_content)

def main():
    script_dir = os.path.dirname(__file__)
    input_dir = os.path.join(script_dir, 'input')
    output_dir = os.path.join(script_dir, 'output')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.lib'):
            print(f"Processing: {filename}")
            split_library_file(os.path.join(input_dir, filename), output_dir)

    print("✅ .lib 文件拆分完成！")

if __name__ == '__main__':
    main()