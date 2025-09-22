import re
import sys


def preprocess(text):
    return re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)


def lcs(a, b):
    m, n = len(a), len(b)
    if m == 0 or n == 0:
        return 0
    dp = [0] * (n + 1)
    for i in range(1, m + 1):
        pre = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if a[i - 1] == b[j - 1]:
                dp[j] = pre + 1
            else:
                if dp[j] < dp[j - 1]:
                    dp[j] = dp[j - 1]
            pre = temp
    return dp[n]


def main():
    if len(sys.argv) != 4:
        print("Usage: python paper_check.py [original_file] [copied_file] [output_file]")
        sys.exit(1)

    original_file = sys.argv[1]
    copied_file = sys.argv[2]
    output_file = sys.argv[3]

    try:
        with open(original_file, 'r', encoding='utf-8') as f:
            original_text = f.read()
        with open(copied_file, 'r', encoding='utf-8') as f:
            copied_text = f.read()
    except Exception as e:
        print(f"Error reading files: {e}")
        sys.exit(1)

    processed_original = preprocess(original_text)
    processed_copied = preprocess(copied_text)

    len_copied = len(processed_copied)
    if len_copied == 0:
        similarity_rate = 0.0
    else:
        lcs_length = lcs(processed_original, processed_copied)
        similarity_rate = lcs_length / len_copied

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("{:.2f}".format(similarity_rate))


if __name__ == '__main__':
    main()
