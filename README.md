
# Aspera FastQ Downloader





这是一个用于从EBI数据库使用Aspera批量下载FastQ文件的Python脚本。

## 功能特点

- 支持并行下载多个FastQ文件
- 使用Aspera高速下载
- 可配置的下载参数
- 支持从TSV文件批量读取下载链接
- 自动创建输出目录

## 依赖要求

- Python 3.6+
- Aspera Connect
- 安装在conda环境中的ascp

## 安装

1. 克隆仓库
```bash
git clone https://github.com/thekingofall/ASCPdown.git

```



2. 确保已安装Aspera Connect并配置好环境

## 使用方法

### 基本用法

```bash
python Ascp_down.py
```

### 命令行参数

```bash
python Ascp_down.py [-h] [--input INPUT] [--output OUTPUT] [--workers WORKERS]
                    [--ascp-key ASCP_KEY] [--ascp-binary ASCP_BINARY] 
                    [--column COLUMN]
```

### 参数说明

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--input` | `-i` | filereport_read_run_PRJNA727602_tsv.txt | 输入的TSV文件路径 |
| `--output` | `-o` | fastq_files | 输出目录 |
| `--workers` | `-w` | 4 | 并行下载的线程数 |
| `--ascp-key` | - | /data1/maolp/mamba/envs/py38/etc/asperaweb_id_dsa.openssh | Aspera密钥路径 |
| `--ascp-binary` | - | /data1/maolp/mamba/envs/py38/bin/ascp | Aspera二进制文件路径 |
| `--column` | `-c` | 6 | TSV文件中fastq_ftp列的索引（从0开始） |

### 使用示例

1. 使用默认参数下载：
```bash
python Ascp_down.py
```

2. 指定自定义参数：
```bash
python Ascp_down.py -i my_data.tsv -o download_dir -w 8 --column 3
```

3. 使用不同的Aspera配置：
```bash
python Ascp_down.py --ascp-key /path/to/key --ascp-binary /path/to/ascp
```

## 输入文件格式

输入的TSV文件应包含fastq_ftp列，格式示例：
```
run_accession    fastq_ftp
SRR14355886      ftp.sra.ebi.ac.uk/vol1/fastq/SRR143/086/SRR14355886/SRR14355886_1.fastq.gz;ftp.sra.ebi.ac.uk/vol1/fastq/SRR143/086/SRR14355886/SRR14355886_2.fastq.gz
```
### 前面步骤

![image](https://github.com/user-attachments/assets/4b81da0f-da58-42da-b024-d1c48df0d0f6)

![image](https://github.com/user-attachments/assets/d3b193c5-404c-4e6f-a2bc-f3513ab89250)

![image](https://github.com/user-attachments/assets/9c6acc3b-5469-47ca-85d3-1161eeecedc1)
