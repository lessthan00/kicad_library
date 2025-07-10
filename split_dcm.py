import os

def read_lines(filename):
    """读取文件并去除每行末尾的换行符"""
    with open(filename, 'r', encoding='latin-1') as f:
        return [line.rstrip('\n') for line in f]

def write_lines(filename, lines):
    """写入文件并在每行后添加换行符"""
    with open(filename, 'w', encoding='latin-1') as f:
        f.write('\n'.join(lines) + '\n')

def split_dcm_file(input_path, output_dir):
    lines = read_lines(input_path)

    components = []
    current_component = None

    for line in lines:
        if line.startswith('$CMP '):
            if current_component is not None:
                components.append(current_component)
            current_component = [line]
        elif line == '$ENDCMP':
            if current_component is not None:
                current_component.append(line)
                components.append(current_component)
                current_component = None
        elif current_component is not None:
            current_component.append(line)

    if current_component is not None:
        components.append(current_component)

    for comp in components:
        name_line = comp[0]
        component_name = name_line.split(maxsplit=1)[1].strip()

        full_content = [
            "EESchema-DOCLIB  Version 2.0",
            "#",
        ]
        full_content.extend(comp)
        full_content.extend([
            "#",
            "#End Doc Library"
        ])

        output_path = os.path.join(output_dir, f"{component_name}.dcm")
        write_lines(output_path, full_content)

def main():
    script_dir = os.path.dirname(__file__)
    input_dir = os.path.join(script_dir, 'input')
    output_dir = os.path.join(script_dir, 'output')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.dcm'):
            print(f"Processing: {filename}")
            split_dcm_file(os.path.join(input_dir, filename), output_dir)

    print("✅ .dcm 文件拆分完成！")

if __name__ == '__main__':
    main()