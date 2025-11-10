import subprocess


def new_private_key(output_file: str = "private_key.pem", key_size: int = 2048) -> None:
    """使用 openssl 生成 RSA 私钥"""
    cmd = ["openssl", "genrsa", "-out", output_file, str(key_size)]
    subprocess.run(cmd, check=True)
    print(f"私钥已生成: {output_file}")
