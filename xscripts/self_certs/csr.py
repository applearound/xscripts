import subprocess
from pathlib import Path


def new_csr(csr_config_file: str, server_pkey_file: str, csr_file: str):
    """
    使用OpenSSL配置文件和已有私钥生成CSR

    Args:
        csr_config_file: 生成CSR文件的OpenSSL配置文件路径
        server_pkey_file: 服务器私钥文件路径
        csr_file:         输出的CSR文件路径
    """
    config_path = Path(csr_config_file)
    pkey_path = Path(server_pkey_file)

    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {csr_config_file}")

    if not pkey_path.exists():
        raise FileNotFoundError(f"私钥文件不存在: {server_pkey_file}")

    try:
        # 使用配置文件和已有私钥生成CSR
        print("正在生成CSR...")
        csr_cmd = [
            "openssl",
            "req",
            "-new",
            "-key",
            server_pkey_file,
            "-out",
            csr_file,
            "-config",
            csr_config_file,
        ]
        subprocess.run(csr_cmd, check=True, capture_output=True)
        print(f"CSR已保存到: {csr_file}")

        # 验证CSR
        print("\n验证CSR内容:")
        verify_cmd = ["openssl", "req", "-text", "-noout", "-in", csr_file]
        result = subprocess.run(verify_cmd, check=True, capture_output=True, text=True)
        print(result.stdout)

        print("\n✓ 成功生成CSR文件!")

    except subprocess.CalledProcessError as e:
        print("错误: OpenSSL命令执行失败")
        if e.stderr:
            print(e.stderr.decode("utf-8"))
    except Exception as e:
        print(f"错误: {str(e)}")
