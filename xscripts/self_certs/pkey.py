import subprocess


def new_private_key(output_file: str = "private.pem", key_size: int = 2048) -> None:
    """使用 openssl 生成 RSA 私钥

    Args:
        output_file: 私钥输出文件路径
        key_size: 私钥大小（位）
    """
    cmd = ["openssl", "genrsa", "-out", output_file, str(key_size)]
    subprocess.run(cmd, check=True)
    print(f"私钥已生成: {output_file}")
