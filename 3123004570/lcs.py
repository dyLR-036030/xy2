# LCS算法模块 - 优化版本，支持长文本
from typing import List, Tuple
import re
from processors import split_into_chunks, merge_chunk_results


def lcs_length_optimized(a: str, b: str) -> int:
    m, n = len(a), len(b)

    if m == 0 or n == 0:
        return 0

    # 确保a是较短的字符串以减少空间使用
    if m > n:
        a, b = b, a
        m, n = n, m

    # 使用一维DP数组，空间复杂度O(min(m, n))
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        prev = 0  # 保存左上角的值 (dp[i-1][j-1])
        for j in range(1, n + 1):
            # 缓存当前值和左边的值，减少数组访问
            current = dp[j]  # dp[i-1][j]
            left = dp[j - 1]  # dp[i][j-1]

            if a[i - 1] == b[j - 1]:
                dp[j] = prev + 1
            else:
                # 使用条件表达式替代max函数
                dp[j] = current if current > left else left

            prev = current  # 更新为当前值，供下一轮使用

    return dp[n]


def lcs_length_chunked(a: str, b: str, chunk_size: int = 1000) -> int:

    if len(a) <= chunk_size and len(b) <= chunk_size:
        return lcs_length_optimized(a, b)

    # 将较长的文本分块
    if len(a) > len(b):
        long_text, short_text = a, b
    else:
        long_text, short_text = b, a

    chunks = split_into_chunks(long_text, chunk_size)

    total_lcs = 0
    for chunk in chunks:
        total_lcs += lcs_length_optimized(short_text, chunk)

    # 由于分块计算可能会重复计算一些匹配，我们需要一个更精确的方法
    # 这里使用一个简化的近似，实际应用中可能需要更复杂的合并策略
    return min(total_lcs, len(short_text))


def calculate_similarity_by_sentence(original: str, copied: str) -> float:
    if not original or not copied:
        return 0.0

    # 分句处理（按句号、问号、感叹号分句）
    def split_sentences(text: str) -> List[str]:
        sentences = re.split(r'[。！？.!?]', text)
        return [s.strip() for s in sentences if s.strip()]

    original_sentences = split_sentences(original)
    copied_sentences = split_sentences(copied)

    if not original_sentences:
        return 0.0

    total_similarity = 0.0
    matched_sentences = 0

    # 对每个原文句子，在抄袭文本中寻找最佳匹配
    for orig_sent in original_sentences:
        if not orig_sent:
            continue

        max_similarity = 0.0
        for copy_sent in copied_sentences:
            if not copy_sent:
                continue

            # 计算两个句子的LCS相似度
            lcs_len = lcs_length_optimized(orig_sent, copy_sent)
            sent_similarity = lcs_len / len(orig_sent) if orig_sent else 0.0

            if sent_similarity > max_similarity:
                max_similarity = sent_similarity

        if max_similarity > 0.3:  # 只考虑相似度超过30%的匹配
            total_similarity += max_similarity
            matched_sentences += 1

    # 如果没有匹配的句子，返回0
    if matched_sentences == 0:
        return 0.0

    # 返回平均相似度
    return total_similarity / len(original_sentences)


def calculate_similarity_chunked(original: str, copied: str, chunk_size: int = 1000) -> float:
    if not original or not copied:
        return 0.0

    # 如果文本较短，直接计算
    if len(original) <= chunk_size and len(copied) <= chunk_size:
        return calculate_similarity(original, copied)

    # 分块处理
    original_chunks = split_into_chunks(original, chunk_size)
    copied_chunks = split_into_chunks(copied, chunk_size)

    chunk_results = []
    chunk_weights = []

    # 计算每块的相似度
    for i, orig_chunk in enumerate(original_chunks):
        max_similarity = 0.0
        for j, copy_chunk in enumerate(copied_chunks):
            similarity = calculate_similarity(orig_chunk, copy_chunk)
            if similarity > max_similarity:
                max_similarity = similarity

        chunk_results.append(max_similarity)
        # 权重可以根据块的重要性调整，这里简单使用等权重
        chunk_weights.append(1.0)

    # 合并结果
    return merge_chunk_results(chunk_results, chunk_weights)


def calculate_similarity(original: str, copied: str) -> float:

    if not original or not copied:
        return 0.0

    # 如果文本较长，使用分块处理
    if len(original) > 2000 or len(copied) > 2000:
        return calculate_similarity_chunked(original, copied)

    # 方法1: 整体LCS相似度
    lcs_len = lcs_length_optimized(original, copied)
    overall_similarity = lcs_len / len(original) if original else 0.0

    # 方法2: 句子级相似度
    sentence_similarity = calculate_similarity_by_sentence(original, copied)

    # 结合两种方法，给予句子级相似度更高权重
    final_similarity = 0.3 * overall_similarity + 0.7 * sentence_similarity

    # 确保结果在0-1范围内
    return max(0.0, min(1.0, final_similarity))
