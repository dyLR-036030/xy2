import sys
import time
from file_io import validate_arguments, read_files, write_result
from processors import preprocess, validate_text_length
from lcs import calculate_similarity  
from config import MAX_TEXT_LENGTH


def main():
    try:
        # 验证参数
        original_file, copied_file, output_file = validate_arguments()

        # 读取文件
        print("正在读取文件...")
        original_text, copied_text = read_files(original_file, copied_file)

        print(f"原文长度: {len(original_text)} 字符")
        print(f"抄袭文本长度: {len(copied_text)} 字符")

        # 验证文本长度（现在只是提示作用）
        if len(original_text) < 10 or len(copied_text) < 10:
            print("提示: 文本长度较短，查重结果仅供参考")
        elif len(original_text) < 100 or len(copied_text) < 100:
            print("提示: 文本长度适中，查重结果较为准确")
        else:
            print("提示: 文本长度充足，查重结果准确度较高")

        # 预处理文本
        print("正在预处理文本...")
        start_time = time.time()
        processed_original = preprocess(original_text)
        processed_copied = preprocess(copied_text)
        preprocess_time = time.time() - start_time

        print(f"预处理完成，耗时: {preprocess_time:.2f}秒")
        print(f"预处理后原文长度: {len(processed_original)} 字符")
        print(f"预处理后抄袭文本长度: {len(processed_copied)} 字符")

        # 计算相似度
        print("正在计算相似度...")
        start_time = time.time()
        similarity_rate = calculate_similarity(processed_original, processed_copied)
        calc_time = time.time() - start_time

        print(f"相似度计算完成，耗时: {calc_time:.2f}秒")

        # 输出结果
        write_result(output_file, similarity_rate)
        print(f"查重完成！相似度: {similarity_rate:.2f}")
        print(f"结果已保存到: {output_file}")

    except ValueError as e:
        print(f"参数错误: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"文件错误: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"IO错误: {e}")
        sys.exit(1)
    except MemoryError as e:
        print(f"内存不足: {e}")
        print("尝试使用更小的分块大小...")
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
