#!/usr/bin/env python3

import subprocess
import argparse
from pathlib import Path

def generate_ca_cert(
    private_key: str,
    config_file: str,
    output_cert: str = "ca_cert.pem",
    days: int = 3650
) -> None:
    """使用 openssl 和配置文件生成 CA 证书"""
    
    # 验证输入文件
    if not Path(private_key).exists():
        raise FileNotFoundError(f"私钥文件不存在: {private_key}")
    
    if not Path(config_file).exists():
        raise FileNotFoundError(f"配置文件不存在: {config_file}")
    
    # 生成 CA 证书
    cmd = [
        "openssl", "req",
        "-new", "-x509",
        "-days", str(days),
        "-key", private_key,
        "-config", config_file,
        "-out", output_cert
    ]
    
    subprocess.run(cmd, check=True)
    print(f"CA 证书已生成: {output_cert}")
    
    # 显示证书信息
    subprocess.run(["openssl", "x509", "-noout", "-text", "-in", output_cert])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="使用 openssl 生成 CA 证书")
    parser.add_argument("-k", "--key", required=True, help="私钥文件路径")
    parser.add_argument("-c", "--config", required=True, help="OpenSSL 配置文件路径")
    parser.add_argument("-o", "--output", default="ca_cert.pem", help="输出证书文件名 (默认: ca_cert.pem)")
    parser.add_argument("-d", "--days", type=int, default=3650, help="证书有效期天数 (默认: 3650)")
    args = parser.parse_args()
    
    generate_ca_cert(args.key, args.config, args.output, args.days)

