import sys
from file_io import validate_arguments, read_files, write_result
from processors import preprocess, validate_text_length
from lcs import calculate_similarity


def main():
    """
    主函数
    """
    try:
        # 验证参数
        original_file, copied_file, output_file = validate_arguments()

        # 读取文件
        original_text, copied_text = read_files(original_file, copied_file)

        # 预处理文本
        processed_original = preprocess(original_text)
        processed_copied = preprocess(copied_text)

        # 验证文本长度
        if not validate_text_length(processed_copied):
            similarity_rate = 0.0
        else:
            # 计算相似度
            similarity_rate = calculate_similarity(processed_original, processed_copied)

        # 输出结果
        write_result(output_file, similarity_rate)
        print(f"查重完成！相似度: {similarity_rate:.2%}")

    except ValueError as e:
        print(f"参数错误: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"文件错误: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"IO错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
