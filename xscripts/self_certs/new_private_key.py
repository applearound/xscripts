#!/usr/bin/env python3

import subprocess
import argparse

def generate_private_key(output_file: str = "private_key.pem", key_size: int = 2048) -> None:
    """使用 openssl 生成 RSA 私钥"""
    cmd = ["openssl", "genrsa", "-out", output_file, str(key_size)]
    subprocess.run(cmd, check=True)
    print(f"私钥已生成: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="使用 openssl 生成 RSA 私钥")
    parser.add_argument("-o", "--output", default="private_key.pem", help="输出文件名 (默认: private_key.pem)")
    parser.add_argument("-s", "--size", type=int, default=2048, help="密钥大小 (默认: 2048)")
    args = parser.parse_args()
    
    generate_private_key(args.output, args.size)
