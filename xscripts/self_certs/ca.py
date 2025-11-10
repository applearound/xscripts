import subprocess
from pathlib import Path


def new_ca_cert(
    ca_pkey_file: str,
    config_file: str,
    output: str = "ca_cert.pem",
    days: int = 3650,
) -> None:
    """使用 openssl 和配置文件生成 CA 证书"""

    # 验证输入文件
    if not Path(ca_pkey_file).exists():
        raise FileNotFoundError(f"私钥文件不存在: {ca_pkey_file}")

    if not Path(config_file).exists():
        raise FileNotFoundError(f"配置文件不存在: {config_file}")

    # 生成 CA 证书
    cmd = [
        "openssl",
        "req",
        "-new",
        "-x509",
        "-days",
        str(days),
        "-key",
        ca_pkey_file,
        "-config",
        config_file,
        "-out",
        output,
    ]

    subprocess.run(cmd, check=True)
    print(f"CA 证书已生成: {output}")

    # 显示证书信息
    subprocess.run(["openssl", "x509", "-noout", "-text", "-in", output])


def verify_certificate(cert_file: str, ca_cert_file: str) -> None:
    """
    验证并显示证书信息

    Args:
        cert_file: 证书文件路径
        ca_cert_file: CA证书文件路径
    """
    print("\n证书信息:")
    print("=" * 60)

    # 显示证书详细信息
    cmd = ["openssl", "x509", "-in", cert_file, "-text", "-noout"]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError:
        print("警告: 无法读取证书信息")

    # 验证证书链
    print("\n验证证书链:")
    print("-" * 60)
    cmd = ["openssl", "verify", "-CAfile", ca_cert_file, cert_file]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("警告: 证书验证失败")
        if e.stdout:
            print(e.stdout.decode("utf-8"))
