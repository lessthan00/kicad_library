import os
import subprocess

# 设置路径
input_dir = "./Source_Symbols"   # 存放 .lib 文件的目录
output_dir = "./get"     # 输出 .kicad_sym 文件的目录

# 创建输出目录（如果不存在）
os.makedirs(output_dir, exist_ok=True)

# 遍历输入目录中的所有 .lib 文件
for filename in os.listdir(input_dir):
    if filename.endswith(".lib"):
        input_path = os.path.join(input_dir, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.kicad_sym")

        # 构造命令
        command = [
            "kicad-cli", "sym", "upgrade",
            "--output", output_path,
            "--force",  # 强制转换，即使已经是旧版格式
            input_path
        ]

        print(f"正在转换: {input_path} -> {output_path}")
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ 转换失败: {e}")

print("✅ 所有文件转换完成。")