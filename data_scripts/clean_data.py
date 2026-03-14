import pandas as pd
import os


def clean_car_data(input_file: str = "temp1.csv", output_file: str = "cleanData.csv"):
    """
    清洗汽车数据CSV文件
    1. 读取CSV文件（兼容gb18030编码）
    2. 删除指定无用列
    3. 删除必填字段为空的行
    4. 保存清洗后的数据

    Args:
        input_file: 输入CSV文件路径
        output_file: 输出清洗后CSV文件路径
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：输入文件 {input_file} 不存在！")
        return

    try:
        # 读取CSV文件，使用gb18030编码，忽略编码错误
        # 注意：error_bad_lines已废弃，改用on_bad_lines
        df = pd.read_csv(
            input_file,
            encoding='gb18030',
            errors='ignore',
            engine='python',
            on_bad_lines=lambda x: None  # 替代废弃的error_bad_lines=False
        )

        print(f"原始数据行数：{len(df)}")

        # 定义需要删除的列名
        cols_to_drop = ['description', 'size', 'county']
        # 按列删除指定列（仅删除存在的列，避免KeyError）
        existing_cols = [col for col in cols_to_drop if col in df.columns]
        df.drop(labels=existing_cols, axis=1, inplace=True)

        # 定义必填字段列表
        required_fields = [
            'id', 'url', 'region', 'region_url', 'price', 'year',
            'manufacturer', 'model', 'condition', 'fuel', 'odometer',
            'title_status', 'transmission', 'VIN', 'drive', 'type',
            'image_url', 'state', 'posting_date'
        ]
        # 仅保留数据中实际存在的必填字段（避免KeyError）
        valid_required_fields = [field for field in required_fields if field in df.columns]

        # 删除必填字段为空的行
        df.dropna(
            subset=valid_required_fields,
            axis=0,  # 按行删除
            how='any',  # 任意必填字段为空就删除
            inplace=True  # 原地修改DataFrame
        )

        print(f"清洗后数据行数：{len(df)}")

        # 保存清洗后的数据，不保留索引列，确保编码正确
        df.to_csv(
            output_file,
            index=False,
            encoding='gb18030'
        )
        print(f"清洗后的数据已保存到：{output_file}")

    except Exception as e:
        print(f"数据清洗过程中出错：{str(e)}")


# 执行数据清洗
if __name__ == "__main__":
    clean_car_data()