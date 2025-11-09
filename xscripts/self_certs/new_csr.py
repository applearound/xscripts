#!/usr/bin/env python3

"""
生成HTTPS服务所需的私钥和CSR文件
"""

import argparse
import subprocess
import sys
from pathlib import Path


def generate_key_and_csr(config_file, key_file, csr_file, key_size=2048):
    """
    使用OpenSSL配置文件生成私钥和CSR
    
    Args:
        config_file: OpenSSL配置文件路径
        key_file: 输出的私钥文件路径
        csr_file: 输出的CSR文件路径
        key_size: 密钥长度，默认2048位
    """
    config_path = Path(config_file)
    
    if not config_path.exists():
        print(f"错误: 配置文件不存在: {config_file}")
        sys.exit(1)
    
    try:
        # 生成私钥
        print(f"正在生成 {key_size} 位私钥...")
        key_cmd = [
            'openssl', 'genrsa',
            '-out', key_file,
            str(key_size)
        ]
        subprocess.run(key_cmd, check=True, capture_output=True)
        print(f"私钥已保存到: {key_file}")
        
        # 使用配置文件生成CSR
        print("正在生成CSR...")
        csr_cmd = [
            'openssl', 'req',
            '-new',
            '-key', key_file,
            '-out', csr_file,
            '-config', config_file
        ]
        subprocess.run(csr_cmd, check=True, capture_output=True)
        print(f"CSR已保存到: {csr_file}")
        
        # 验证CSR
        print("\n验证CSR内容:")
        verify_cmd = ['openssl', 'req', '-text', '-noout', '-in', csr_file]
        result = subprocess.run(verify_cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        
        print("\n✓ 成功生成私钥和CSR文件!")
        
    except subprocess.CalledProcessError as e:
        print(f"错误: OpenSSL命令执行失败")
        if e.stderr:
            print(e.stderr.decode('utf-8'))
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='生成HTTPS服务所需的私钥和CSR文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s -c openssl.cnf -k server.key -r server.csr
  %(prog)s -c openssl.cnf -k server.key -r server.csr -s 4096
        """
    )
    
    parser.add_argument(
        '-c', '--config',
        required=True,
        help='OpenSSL配置文件路径'
    )
    parser.add_argument(
        '-k', '--key',
        default='server.key',
        help='输出的私钥文件名 (默认: server.key)'
    )
    parser.add_argument(
        '-r', '--csr',
        default='server.csr',
        help='输出的CSR文件名 (默认: server.csr)'
    )
    parser.add_argument(
        '-s', '--key-size',
        type=int,
        default=2048,
        choices=[2048, 4096],
        help='密钥长度 (默认: 2048)'
    )
    
    args = parser.parse_args()
    
    generate_key_and_csr(
        args.config,
        args.key,
        args.csr,
        args.key_size
    )


if __name__ == '__main__':
    main()
