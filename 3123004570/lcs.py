# LCS算法模块
from typing import Tuple


def lcs_optimized(a: str, b: str) -> int:
    """
    优化的LCS算法实现，使用滚动数组降低空间复杂度

    Args:
        a: 字符串A
        b: 字符串B

    Returns:
        LCS长度
    """
    m, n = len(a), len(b)

    # 处理边界情况
    if m == 0 or n == 0:
        return 0

    # 确保a是较短的字符串以减少空间使用
    if m > n:
        a, b = b, a
        m, n = n, m

    # 使用一维DP数组，空间复杂度O(min(m, n))
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        prev = 0  # 保存左上角的值
        for j in range(1, n + 1):
            temp = dp[j]  # 保存当前值，供下一次迭代使用
            if a[i - 1] == b[j - 1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = temp

    return dp[n]


def calculate_similarity(original: str, copied: str) -> float:
    """
    计算相似度比率

    Args:
        original: 原文
        copied: 抄袭文本

    Returns:
        相似度比率 (0.0 - 1.0)
    """
    if not copied:
        return 0.0

    lcs_length = lcs_optimized(original, copied)
    return lcs_length / len(copied)
