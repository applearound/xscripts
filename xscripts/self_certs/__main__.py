import argparse

from .ca import new_ca_cert
from .cert import new_ca_signed_cert
from .csr import new_csr
from .pkey import new_private_key


def _init_pkey_parser(pkey_parser: argparse.ArgumentParser) -> None:
    pkey_parser.add_argument(
        "-o",
        "--output",
        default="private_key.pem",
        help="输出文件名 (默认: private_key.pem)",
    )
    pkey_parser.add_argument(
        "-s", "--size", type=int, default=2048, help="密钥大小 (默认: 2048)"
    )


def _init_ca_parser(ca_parser: argparse.ArgumentParser) -> None:
    ca_parser.add_argument("-k", "--key", required=True, help="私钥文件路径")
    ca_parser.add_argument("-c", "--config", required=True, help="OpenSSL 配置文件路径")
    ca_parser.add_argument(
        "-o",
        "--output",
        default="ca_cert.pem",
        help="输出证书文件名 (默认: ca_cert.pem)",
    )
    ca_parser.add_argument(
        "-d", "--days", type=int, default=3650, help="证书有效期天数 (默认: 3650)"
    )


def _init_csr_parser(csr_parser: argparse.ArgumentParser) -> None:
    csr_parser.add_argument("-c", "--config", required=True, help="OpenSSL配置文件路径")
    csr_parser.add_argument(
        "-k", "--key", default="server.key", help="输出的私钥文件名 (默认: server.key)"
    )
    csr_parser.add_argument(
        "-r", "--csr", default="server.csr", help="输出的CSR文件名 (默认: server.csr)"
    )


def _init_cert_parser(cert_parser: argparse.ArgumentParser) -> None:
    cert_parser.add_argument("-r", "--csr", required=True, help="CSR文件路径")
    cert_parser.add_argument("--ca-cert", required=True, help="CA证书文件路径")
    cert_parser.add_argument("--ca-key", required=True, help="CA私钥文件路径")
    cert_parser.add_argument(
        "-o",
        "--output",
        default="server.crt",
        help="输出的证书文件名 (默认: server.crt)",
    )
    cert_parser.add_argument(
        "-d", "--days", type=int, default=365, help="证书有效期（天）(默认: 365)"
    )
    cert_parser.add_argument(
        "-c", "--config", help="OpenSSL配置文件（用于添加扩展，如SAN）"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="自签证书工具集")

    subparsers = parser.add_subparsers(dest="command", required=True)

    pkey_parser = subparsers.add_parser("new_pkey", help="生成RSA私钥")
    ca_parser = subparsers.add_parser("new_ca", help="生成CA证书")
    csr_parser = subparsers.add_parser("new_csr", help="生成私钥和CSR文件")
    cert_parser = subparsers.add_parser("new_cert", help="从CSR生成CA签名证书")

    _init_pkey_parser(pkey_parser)
    _init_ca_parser(ca_parser)
    _init_csr_parser(csr_parser)
    _init_cert_parser(cert_parser)

    args = parser.parse_args()

    if args.command == "new_pkey":
        new_private_key(args.output, args.size)
    elif args.command == "new_ca":
        new_ca_cert(args.key, args.config, args.output, args.days)
    elif args.command == "new_csr":
        new_csr(args.config, args.key, args.csr)
    elif args.command == "new_cert":
        new_ca_signed_cert(
            args.csr,
            args.ca_cert,
            args.ca_key,
            args.output,
            args.days,
            args.config,
        )
