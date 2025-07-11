import os
import re

def clean_filename(name):
    """清理文件名中的非法字符"""
    # 替换Windows文件名中不允许的字符
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    # 移除开头和结尾的空格和点
    name = name.strip('. ')
    # 如果名字为空，使用默认名
    if not name:
        name = "unnamed_component"
    return name

def read_lines(filename):
    # 先尝试UTF-8，失败后尝试Latin-1
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.rstrip('\n') for line in file]
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin-1') as file:
            return [line.rstrip('\n') for line in file]

def write_lines(filename, lines):
    # 始终以UTF-8编码写入
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
            # 清理组件名称用于文件名
            clean_name = clean_filename(component_name)
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
            components.append((component_name, clean_name, current_component))
        else:
            i += 1

    # 写入每个组件
    for original_name, clean_name, comp_lines in components:
        full_content = standard_header + comp_lines + standard_footer
        output_path = os.path.join(output_dir, f"{clean_name}.lib")
        try:
            write_lines(output_path, full_content)
            print(f"成功保存: {clean_name}.lib (原名称: {original_name})")
        except Exception as e:
            print(f"无法保存 {clean_name}.lib: {str(e)}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, 'input')
    output_dir = os.path.join(script_dir, 'output')

    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"⚠️ 已创建输入目录: {input_dir}")
        print("请将.lib文件放入此目录后重新运行脚本。")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    lib_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.lib')]
    
    if not lib_files:
        print("⚠️ 输入目录中没有找到.lib文件。")
        return

    for filename in lib_files:
        print(f"正在处理: {filename}")
        split_library_file(os.path.join(input_dir, filename), output_dir)

    print("✅ .lib文件拆分完成!")

if __name__ == '__main__':
    main()