# 文本处理模块
import re
from config import PREPROCESS_PATTERN, MIN_TEXT_LENGTH, MAX_TEXT_LENGTH, CHUNK_SIZE, OVERLAP_SIZE


def preprocess(text: str) -> str:
    """
    预处理文本，移除非中文字母数字的字符，并转换为小写

    Args:
        text: 输入文本

    Returns:
        处理后的文本
    """
    # 移除所有非中文字母数字的字符
    cleaned_text = PREPROCESS_PATTERN.sub('', text)
    # 转换为小写以消除大小写差异
    return cleaned_text.lower()


def validate_text_length(text: str, min_length: int = MIN_TEXT_LENGTH) -> bool:
    return len(text) >= min_length


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP_SIZE) -> list:
    """
    将长文本分割成小块，用于分段处理

    Args:
        text: 输入文本
        chunk_size: 每块大小
        overlap: 重叠大小

    Returns:
        文本块列表
    """
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)

        # 如果已经到文本末尾，跳出循环
        if end == len(text):
            break

        # 移动起始位置，考虑重叠
        start += chunk_size - overlap

    return chunks


def merge_chunk_results(chunk_results: list, weights: list = None) -> float:
    """
    合并分块处理的结果

    Args:
        chunk_results: 各块的相似度结果
        weights: 各块的权重（默认为等权重）

    Returns:
        合并后的相似度
    """
    if not chunk_results:
        return 0.0

    if weights is None:
        weights = [1.0] * len(chunk_results)

    # 归一化权重
    total_weight = sum(weights)
    if total_weight == 0:
        return 0.0

    normalized_weights = [w / total_weight for w in weights]

    # 计算加权平均
    weighted_sum = sum(result * weight for result, weight in zip(chunk_results, normalized_weights))

    return weighted_sum
