import subprocess
from typing import Optional


def new_ca_signed_cert(
    csr_file: str,
    ca_cert_file: str,
    ca_key_file: str,
    cert_file: str,
    days: int = 365,
    config_file: Optional[str] = None,
) -> None:
    """
    使用CA证书签名生成证书

    Args:
        csr_file: CSR文件路径
        ca_cert_file: CA证书文件路径
        ca_key_file: CA私钥文件路径
        cert_file: 输出的证书文件路径
        days: 证书有效期（天）
        config_file: OpenSSL配置文件（可选，用于扩展）
    """
    print(f"正在使用CA签名生成证书（有效期 {days} 天）...")

    cmd = [
        "openssl",
        "x509",
        "-req",
        "-in",
        csr_file,
        "-CA",
        ca_cert_file,
        "-CAkey",
        ca_key_file,
        "-CAcreateserial",
        "-out",
        cert_file,
        "-days",
        str(days),
    ]

    # 如果提供了配置文件，添加扩展
    if config_file:
        cmd.extend(["-extensions", "v3_req", "-extfile", config_file])

    # 添加 copy_extensions 以复制CSR中的扩展，同时自动添加 authorityKeyIdentifier
    cmd.extend(["-copy_extensions", "copy"])

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✓ CA签名证书已保存到: {cert_file}")
    except subprocess.CalledProcessError as e:
        if e.stderr:
            print(e.stderr.decode("utf-8"))
