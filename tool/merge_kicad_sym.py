import os

# 设置路径：当前目录下的 b 子目录
dir_path = os.path.join('.', 'b')
output_file = 'merged_library.kicad_sym'

# 全局头部和尾部
header = '''(kicad_symbol_lib
	(version 20241209)
	(generator "kicad_symbol_editor")
	(generator_version "9.0")
'''

footer = ')'

all_symbols = []

# 遍历目录中的 .kicad_sym 文件
for filename in sorted(os.listdir(dir_path)):
    if filename.endswith('.kicad_sym'):
        file_path = os.path.join(dir_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 找到第一个 (symbol 的位置
        start_index = None
        for i, line in enumerate(lines):
            if '(symbol' in line.strip():
                start_index = i
                break
        
        if start_index is None:
            print(f"⚠️ 警告：{filename} 中未找到任何 symbol 定义，跳过。")
            continue

        # 找到最后一个 ")"
        end_index = None
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() == ')':
                end_index = i
                break
        
        if end_index is None:
            print(f"⚠️ 警告：{filename} 缺少结尾的 ')', 使用全部内容。")
            end_index = len(lines)

        # 提取从第一个 symbol 到倒数第一个 ) 之前的内容
        content = lines[start_index:end_index]
        all_symbols.extend(content)

# 写入输出文件
with open(output_file, 'w', encoding='utf-8') as out_f:
    out_f.write(header)
    out_f.writelines(all_symbols)
    out_f.write(footer)

print(f"✅ 合并完成，结果保存在：{os.path.abspath(output_file)}")