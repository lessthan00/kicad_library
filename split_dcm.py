import os
import re

def read_file_with_encoding(file_path):
    encodings = ['latin1', 'utf-8', 'utf-8-sig', 'cp1252']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                return f.readlines()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"无法用任何编码打开文件: {file_path}")

def split_dcm_file(file_path, output_dir):
    print(f"🔧 开始处理: {file_path}")
    try:
        lines = read_file_with_encoding(file_path)
    except Exception as e:
        print(f"❌ 错误：无法读取文件 {file_path} - {e}")
        return

    # 提取 header（第一个 $CMP 之前的所有行）
    header_end_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith('$CMP'):
            header_end_index = i
            break
    header = [line.rstrip('\n') for line in lines[:header_end_index]]

    # 提取所有 component
    components = []
    current_component = []
    inside = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('$CMP'):
            inside = True
            current_component = [line.rstrip('\n')]
        elif stripped.startswith('$ENDCMP'):
            current_component.append(line.rstrip('\n'))
            components.append(current_component)
            inside = False
        elif inside:
            current_component.append(line.rstrip('\n'))

    # 提取 footer（最后一个 $ENDCMP 之后的内容）
    last_footer_start = len(lines)
    for i in reversed(range(len(lines))):
        if lines[i].strip().startswith('$ENDCMP'):
            last_footer_start = i + 1
            break
    footer = [line.rstrip('\n') for line in lines[last_footer_start:]]

    print(f"✅ 找到 {len(components)} 个元件")

    for comp in components:
        first_line = comp[0]
        match = re.match(r'\$CMP\s+(\S+)', first_line)
        if not match:
            print("⚠️ 跳过无效元件（找不到名称）")
            continue
        name = match.group(1)

        output_file = os.path.join(output_dir, f"{name}.dcm")
        if os.path.exists(output_file):
            print(f"🔁 已存在，跳过: {output_file}")
            continue

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(header) + '\n')
            f.write('\n'.join(comp) + '\n')
            f.write('\n'.join(footer) + '\n')

        print(f"💾 已保存: {output_file}")

def main():
    input_dir = 'lib'
    output_dir = 'get'
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.dcm'):
            filepath = os.path.join(input_dir, filename)
            try:
                split_dcm_file(filepath, output_dir)
            except Exception as e:
                print(f"⚠️ 处理失败: {filename} - {e}")

if __name__ == '__main__':
    main()