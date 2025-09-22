# 文件读写模块
import sys
from typing import Tuple
from config import FILE_ENCODING


def read_files(original_path: str, copied_path: str) -> Tuple[str, str]:
    """
    读取原始文件和抄袭文件

    Args:
        original_path: 原始文件路径
        copied_path: 抄袭文件路径

    Returns:
        Tuple[原始文本, 抄袭文本]

    Raises:
        FileNotFoundError: 文件不存在
        IOError: 文件读取错误
    """
    try:
        with open(original_path, 'r', encoding=FILE_ENCODING) as f:
            original_text = f.read()

        with open(copied_path, 'r', encoding=FILE_ENCODING) as f:
            copied_text = f.read()

        return original_text, copied_text

    except FileNotFoundError as e:
        raise FileNotFoundError(f"文件未找到: {e.filename}") from e
    except Exception as e:
        raise IOError(f"文件读取错误: {e}") from e


def write_result(output_path: str, similarity: float) -> None:
    """
    将相似度结果写入文件

    Args:
        output_path: 输出文件路径
        similarity: 相似度值
    """
    from config import SIMILARITY_FORMAT

    try:
        with open(output_path, 'w', encoding=FILE_ENCODING) as f:
            f.write(SIMILARITY_FORMAT.format(similarity))
    except Exception as e:
        raise IOError(f"结果写入失败: {e}") from e


def validate_arguments() -> Tuple[str, str, str]:
    """
    验证命令行参数

    Returns:
        Tuple[原始文件路径, 抄袭文件路径, 输出文件路径]

    Raises:
        ValueError: 参数数量不正确
    """
    if len(sys.argv) != 4:
        raise ValueError("用法: python main.py [原文文件] [抄袭文件] [输出文件]")

    return sys.argv[1], sys.argv[2], sys.argv[3]
