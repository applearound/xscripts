#!/usr/bin/env python3
"""
从CSR文件生成HTTPS服务证书
使用CA证书签名
"""

import argparse
import subprocess
import sys
from pathlib import Path


def generate_ca_signed_cert(csr_file, ca_cert_file, ca_key_file, cert_file, 
                            days=365, config_file=None):
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
        'openssl', 'x509',
        '-req',
        '-in', csr_file,
        '-CA', ca_cert_file,
        '-CAkey', ca_key_file,
        '-CAcreateserial',
        '-out', cert_file,
        '-days', str(days)
    ]
    
    # 如果提供了配置文件，添加扩展
    if config_file:
        cmd.extend(['-extensions', 'req_ext', '-extfile', config_file])
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✓ CA签名证书已保存到: {cert_file}")
    except subprocess.CalledProcessError as e:
        print(f"错误: 生成证书失败")
        if e.stderr:
            print(e.stderr.decode('utf-8'))
        sys.exit(1)


def verify_certificate(cert_file, ca_cert_file):
    """
    验证并显示证书信息
    
    Args:
        cert_file: 证书文件路径
        ca_cert_file: CA证书文件路径
    """
    print("\n证书信息:")
    print("=" * 60)
    
    # 显示证书详细信息
    cmd = ['openssl', 'x509', '-in', cert_file, '-text', '-noout']
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError:
        print("警告: 无法读取证书信息")
    
    # 验证证书链
    print("\n验证证书链:")
    print("-" * 60)
    cmd = ['openssl', 'verify', '-CAfile', ca_cert_file, cert_file]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"警告: 证书验证失败")
        if e.stdout:
            print(e.stdout.decode('utf-8'))


def check_file_exists(filepath, file_type):
    """检查文件是否存在"""
    if not Path(filepath).exists():
        print(f"错误: {file_type}不存在: {filepath}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='从CSR文件生成HTTPS服务证书（使用CA签名）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  %(prog)s -r server.csr --ca-cert ca.crt --ca-key ca.key -o server.crt
  
  # 指定有效期和配置文件
  %(prog)s -r server.csr --ca-cert ca.crt --ca-key ca.key -o server.crt -d 730 -c openssl.cnf
        """
    )
    
    parser.add_argument(
        '-r', '--csr',
        required=True,
        help='CSR文件路径'
    )
    parser.add_argument(
        '--ca-cert',
        required=True,
        help='CA证书文件路径'
    )
    parser.add_argument(
        '--ca-key',
        required=True,
        help='CA私钥文件路径'
    )
    parser.add_argument(
        '-o', '--output',
        default='server.crt',
        help='输出的证书文件名 (默认: server.crt)'
    )
    parser.add_argument(
        '-d', '--days',
        type=int,
        default=365,
        help='证书有效期（天）(默认: 365)'
    )
    parser.add_argument(
        '-c', '--config',
        help='OpenSSL配置文件（用于添加扩展，如SAN）'
    )
    
    args = parser.parse_args()
    
    # 检查所有必需文件
    check_file_exists(args.csr, 'CSR文件')
    check_file_exists(args.ca_cert, 'CA证书文件')
    check_file_exists(args.ca_key, 'CA私钥文件')
    
    # 检查配置文件
    if args.config:
        check_file_exists(args.config, '配置文件')
    
    # 生成CA签名证书
    generate_ca_signed_cert(
        args.csr,
        args.ca_cert,
        args.ca_key,
        args.output,
        args.days,
        args.config
    )
    
    # 验证证书
    verify_certificate(args.output, args.ca_cert)
    
    print("\n✓ 证书生成完成!")


if __name__ == '__main__':
    main()
