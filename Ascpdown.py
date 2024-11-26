#!/usr/bin/env python3

import os
import concurrent.futures
import subprocess

# 使用conda环境中的ascp
ASCP_KEY = os.path.expanduser("/data1/maolp/mamba/envs/py38/etc/asperaweb_id_dsa.openssh")
ASCP_BINARY = os.path.expanduser("/data1/maolp/mamba/envs/py38/bin/ascp")
ASCP_OPTIONS = "-QT -l 300m -P33001 -k1"

def download_with_ascp(url_pair):
    """使用ascp下载一对fastq文件"""
    for url in url_pair.split(';'):
        # 转换URL格式
        aspera_url = f"era-fasp@fasp.sra.ebi.ac.uk:/{'/'.join(url.split('/')[1:])}"
        filename = url.split('/')[-1]
        
        # 构建ascp命令
        cmd = f"{ASCP_BINARY} {ASCP_OPTIONS} -i {ASCP_KEY} {aspera_url} ."
        
        try:
            print(f"Downloading {filename}...")
            print(f"Command: {cmd}")
            subprocess.run(cmd, shell=True, check=True)
            print(f"Successfully downloaded {filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading {filename}: {e}")

def main():
    # 创建输出目录
    os.makedirs("fastq_files", exist_ok=True)
    os.chdir("fastq_files")
    
    # 读取并解析TSV文件
    with open("filereport_read_run_PRJNA727602_tsv.txt") as f:
        # 跳过表头
        next(f)
        # 获取所有fastq_ftp列
        fastq_urls = [line.strip().split('\t')[6] for line in f if line.strip()]
    
    # 使用线程池并行下载
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_with_ascp, fastq_urls)

if __name__ == "__main__":
    main()
