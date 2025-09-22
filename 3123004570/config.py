# 配置文件
import re

# 预处理正则表达式模式 - 保留中文字符、英文字母和数字
PREPROCESS_PATTERN = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9]')

# 文件编码
FILE_ENCODING = 'utf-8'


SIMILARITY_FORMAT = "{:.2f}"

# 最小文本长度
MIN_TEXT_LENGTH = 10

# 最大文本长度 (3万字)
MAX_TEXT_LENGTH = 30000

# 分块大小 (用于处理长文本)
CHUNK_SIZE = 1000

# 重叠窗口大小 (确保边界匹配)
OVERLAP_SIZE = 100
