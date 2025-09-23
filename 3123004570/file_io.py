# 文件读写模块
import sys
from typing import Tuple
from config import FILE_ENCODING, MAX_TEXT_LENGTH


def read_files(original_path: str, copied_path: str) -> Tuple[str, str]:
    try:
        with open(original_path, 'r', encoding=FILE_ENCODING) as f:
            original_text = f.read().strip()

        with open(copied_path, 'r', encoding=FILE_ENCODING) as f:
            copied_text = f.read().strip()

        # 检查文本长度（只进行截取，不阻止处理）
        if len(original_text) > MAX_TEXT_LENGTH:
            print(f"警告: 原文长度({len(original_text)})超过限制，将截取前{MAX_TEXT_LENGTH}字符")
            original_text = original_text[:MAX_TEXT_LENGTH]

        if len(copied_text) > MAX_TEXT_LENGTH:
            print(f"警告: 抄袭文本长度({len(copied_text)})超过限制，将截取前{MAX_TEXT_LENGTH}字符")
            copied_text = copied_text[:MAX_TEXT_LENGTH]

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
            # 直接输出小数点后两位的格式，如：0.78
            f.write(SIMILARITY_FORMAT.format(similarity))
    except Exception as e:
        raise IOError(f"结果写入失败: {e}") from e


def validate_arguments() -> Tuple[str, str, str]:
    if len(sys.argv) != 4:
        raise ValueError("用法: python main.py [原文文件] [抄袭文件] [输出文件]")
    return sys.argv[1], sys.argv[2], sys.argv[3]
