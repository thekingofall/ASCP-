#!/usr/bin/env python3

import os
import concurrent.futures
import subprocess
import argparse

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='使用Aspera下载fastq文件')
    parser.add_argument('--input', '-i', 
                        default="filereport_read_run_PRJNA727602_tsv.txt",
                        help='输入的TSV文件路径')
    parser.add_argument('--output', '-o', 
                        default="fastq_files",
                        help='输出目录')
    parser.add_argument('--workers', '-w', 
                        type=int, default=4,
                        help='并行下载的线程数')
    parser.add_argument('--ascp-key', 
                        default="/data1/maolp/mamba/envs/py38/etc/asperaweb_id_dsa.openssh",
                        help='Aspera密钥路径')
    parser.add_argument('--ascp-binary', 
                        default="/data1/maolp/mamba/envs/py38/bin/ascp",
                        help='Aspera二进制文件路径')
    parser.add_argument('--column', '-c', 
                        type=int, default=6,
                        help='TSV文件中fastq_ftp列的索引（从0开始）')
    return parser.parse_args()

def download_with_ascp(url_pair, ascp_key, ascp_binary):
    """使用ascp下载一对fastq文件"""
    ASCP_OPTIONS = "-QT -l 300m -P33001 -k1"
    
    for url in url_pair.split(';'):
        # 转换URL格式
        aspera_url = f"era-fasp@fasp.sra.ebi.ac.uk:/{'/'.join(url.split('/')[1:])}"
        filename = url.split('/')[-1]
        
        # 构建ascp命令
        cmd = f"{ascp_binary} {ASCP_OPTIONS} -i {ascp_key} {aspera_url} ."
        
        try:
            print(f"下载文件: {filename}...")
            print(f"执行命令: {cmd}")
            subprocess.run(cmd, shell=True, check=True)
            print(f"成功下载: {filename}")
        except subprocess.CalledProcessError as e:
            print(f"下载错误 {filename}: {e}")

def main():
    args = parse_args()
    
    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)
    os.chdir(args.output)
    
    # 读取并解析TSV文件
    with open(args.input) as f:
        # 跳过表头
        next(f)
        # 获取所有fastq_ftp列
        fastq_urls = [line.strip().split('\t')[args.column] for line in f if line.strip()]
    
    # 使用线程池并行下载
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        download_tasks = [
            executor.submit(download_with_ascp, url, args.ascp_key, args.ascp_binary)
            for url in fastq_urls
        ]
        concurrent.futures.wait(download_tasks)

if __name__ == "__main__":
    main()
