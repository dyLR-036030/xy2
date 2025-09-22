# 配置文件
import re

# 预处理正则表达式模式
PREPROCESS_PATTERN = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9]')

# 文件编码
FILE_ENCODING = 'utf-8'

# 相似度输出格式
SIMILARITY_FORMAT = "{:.2f}"
