from typing import List, Tuple
import re
from functools import lru_cache
from processors import split_into_chunks, merge_chunk_results


@lru_cache(maxsize=500)
def lcs_length_optimized(a: str, b: str) -> int:
    """
    优化版LCS计算，添加缓存和快速检查
    """
    # 快速检查1: 空字符串
    if not a or not b:
        return 0

    # 快速检查2: 完全相同字符串
    if a == b:
        return len(a)

    # 快速检查3: 一个字符串是另一个的子串
    if a in b:
        return len(a)
    if b in a:
        return len(b)

    # 确保a是较短的字符串以减少空间使用
    if len(a) > len(b):
        a, b = b, a

    m, n = len(a), len(b)

    # 对于超长文本使用近似算法
    if m > 2000 or n > 2000:
        return approximate_lcs(a, b)

    # 使用一维DP数组，空间复杂度O(min(m, n))
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        prev = 0  # 保存左上角的值 (dp[i-1][j-1])
        for j in range(1, n + 1):
            current = dp[j]  # dp[i-1][j]
            left = dp[j - 1]  # dp[i][j-1]

            if a[i - 1] == b[j - 1]:
                dp[j] = prev + 1
            else:
                dp[j] = current if current > left else left
            prev = current

    return dp[n]


def approximate_lcs(a: str, b: str, k: int = 4) -> int:
    """
    使用k-gram近似计算LCS，适用于超长文本
    """
    if len(a) > len(b):
        a, b = b, a

    def get_kgrams(text: str, k: int) -> set:
        """获取文本的所有k-gram"""
        return {text[i:i + k] for i in range(len(text) - k + 1)}

    # 获取k-gram集合
    a_grams = get_kgrams(a, k)
    b_grams = get_kgrams(b, k)

    # 计算共同k-gram数量
    common_grams = a_grams & b_grams

    # 近似LCS长度
    return min(len(common_grams) * k, len(a))


def calculate_similarity_by_sentence_optimized(original: str, copied: str) -> float:
    """
    优化版句子级相似度计算，减少不必要的LCS计算
    """
    if not original or not copied:
        return 0.0

    # 高效分句函数
    def split_sentences(text: str) -> List[str]:
        # 统一分隔符后分割
        text = text.replace('。', '.').replace('！', '!').replace('？', '?')
        sentences = re.split(r'[.!?]', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]  # 过滤过短句子

    original_sentences = split_sentences(original)
    copied_sentences = split_sentences(copied)

    if not original_sentences or not copied_sentences:
        return 0.0

    total_similarity = 0.0
    matched_sentences = 0

    # 预处理：计算句子长度和哈希，用于快速匹配
    copied_sentence_info = []
    for sent in copied_sentences:
        if len(sent) >= 10:  # 只处理足够长的句子
            copied_sentence_info.append({
                'text': sent,
                'length': len(sent),
                'hash': hash(sent)
            })

    for orig_sent in original_sentences:
        if len(orig_sent) < 10:  # 跳过过短句子
            continue

        orig_length = len(orig_sent)
        orig_hash = hash(orig_sent)
        max_similarity = 0.0

        # 快速匹配阶段1: 完全相同的句子
        for copy_info in copied_sentence_info:
            if copy_info['hash'] == orig_hash and copy_info['text'] == orig_sent:
                max_similarity = 1.0
                break

        if max_similarity == 1.0:
            total_similarity += max_similarity
            matched_sentences += 1
            continue

        # 快速匹配阶段2: 长度相近的句子才进行详细比较
        for copy_info in copied_sentence_info:
            copy_sent = copy_info['text']
            copy_length = copy_info['length']

            # 长度差异过大则跳过（优化关键！）
            length_ratio = min(orig_length, copy_length) / max(orig_length, copy_length)
            if length_ratio < 0.6:  # 长度差异超过40%则跳过
                continue

            # 快速相似度估算（基于字符集合）
            if quick_similarity_check(orig_sent, copy_sent) < 0.3:
                continue

            # 最终使用LCS计算精确相似度
            lcs_len = lcs_length_optimized(orig_sent, copy_sent)
            sent_similarity = lcs_len / orig_length

            if sent_similarity > max_similarity:
                max_similarity = sent_similarity
                if max_similarity > 0.8:  # 达到高相似度提前终止
                    break

        if max_similarity > 0.3:
            total_similarity += max_similarity
            matched_sentences += 1

    # 返回平均相似度
    return total_similarity / len(original_sentences) if matched_sentences > 0 else 0.0


def quick_similarity_check(a: str, b: str) -> float:
    """
    快速相似度估算，用于预筛选
    基于字符重叠率的快速计算，时间复杂度O(n)
    """
    if not a or not b:
        return 0.0

    # 使用滑动窗口计算字符重叠率
    shorter, longer = (a, b) if len(a) <= len(b) else (b, a)

    char_count_a = {}
    for char in a:
        char_count_a[char] = char_count_a.get(char, 0) + 1

    char_count_b = {}
    for char in b:
        char_count_b[char] = char_count_b.get(char, 0) + 1

    # 计算共同字符数量
    common_chars = 0
    for char in char_count_a:
        if char in char_count_b:
            common_chars += min(char_count_a[char], char_count_b[char])

    total_chars = len(a) + len(b) - common_chars
    return common_chars / total_chars if total_chars > 0 else 0.0


def calculate_similarity_chunked_optimized(original: str, copied: str, chunk_size: int = 2000) -> float:
    """
    优化版分块处理
    """
    if not original or not copied:
        return 0.0

    # 如果文本较短，直接计算
    if len(original) <= chunk_size and len(copied) <= chunk_size:
        return calculate_similarity_optimized(original, copied)

    # 优化分块策略：根据文本长度动态调整块大小
    avg_length = (len(original) + len(copied)) / 2
    if avg_length > 20000:
        chunk_size = 3000
    elif avg_length > 50000:
        chunk_size = 5000

    # 分块处理
    original_chunks = split_into_chunks(original, chunk_size)
    copied_chunks = split_into_chunks(copied, chunk_size)

    chunk_results = []
    chunk_weights = []

    # 为每个原文块寻找最佳匹配的抄袭块
    for i, orig_chunk in enumerate(original_chunks):
        max_similarity = 0.0

        # 限制每个原文块比较的抄袭块数量（优化关键！）
        max_comparisons = min(5, len(copied_chunks))  # 最多比较5个块

        for j in range(max_comparisons):
            if j >= len(copied_chunks):
                break

            copy_chunk = copied_chunks[j]
            similarity = calculate_similarity_optimized(orig_chunk, copy_chunk)
            if similarity > max_similarity:
                max_similarity = similarity
                if max_similarity > 0.9:  # 高相似度提前终止
                    break

        chunk_results.append(max_similarity)
        # 根据块长度设置权重
        chunk_weights.append(len(orig_chunk))

    # 合并结果
    return merge_chunk_results(chunk_results, chunk_weights)


def calculate_similarity_optimized(original: str, copied: str) -> float:
    """
    优化版相似度计算主函数
    """
    if not original or not copied:
        return 0.0

    # 快速检查：完全相同的文本
    if original == copied:
        return 1.0

    # 动态选择计算策略
    text_length = max(len(original), len(copied))

    if text_length > 10000:
        # 超长文本使用分块+近似算法
        return calculate_similarity_chunked_optimized(original, copied)
    elif text_length > 5000:
        # 长文本使用分块处理
        return calculate_similarity_chunked_optimized(original, copied, chunk_size=1500)
    else:
        # 短文本使用精确计算
        return calculate_similarity_precise(original, copied)


def calculate_similarity_precise(original: str, copied: str) -> float:
    """
    精确相似度计算（用于短文本）
    """
    # 方法1: 整体LCS相似度
    lcs_len = lcs_length_optimized(original, copied)
    overall_similarity = lcs_len / len(original) if original else 0.0

    # 方法2: 句子级相似度
    sentence_similarity = calculate_similarity_by_sentence_optimized(original, copied)

    # 智能权重分配：根据文本长度调整权重
    text_length = len(original)
    if text_length < 100:
        # 短文本更依赖整体相似度
        sentence_weight = 0.4
        overall_weight = 0.6
    elif text_length < 1000:
        # 中等文本平衡两种方法
        sentence_weight = 0.6
        overall_weight = 0.4
    else:
        # 长文本更依赖句子级相似度
        sentence_weight = 0.7
        overall_weight = 0.3

    final_similarity = (overall_weight * overall_similarity +
                        sentence_weight * sentence_similarity)

    # 确保结果在0-1范围内
    return max(0.0, min(1.0, final_similarity))


# 保持原有函数接口兼容性
def calculate_similarity(original: str, copied: str) -> float:
    """对外接口，保持兼容"""
    return calculate_similarity_optimized(original, copied)


def calculate_similarity_by_sentence(original: str, copied: str) -> float:
    """对外接口，保持兼容"""
    return calculate_similarity_by_sentence_optimized(original, copied)


def calculate_similarity_chunked(original: str, copied: str, chunk_size: int = 1000) -> float:
    """对外接口，保持兼容"""
    return calculate_similarity_chunked_optimized(original, copied, chunk_size)
