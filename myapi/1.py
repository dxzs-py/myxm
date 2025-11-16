import math


def dm_to_decimal(degree_minute):
    """
    将度分格式(如37.30表示37度30分)转换为十进制度格式
    例如: 37.30 -> 37 + 30/60 = 37.5
    """
    # 分离整数部分(度)和小数部分(分)
    degrees = int(degree_minute)
    minutes = degree_minute - degrees

    # 将小数部分转换回实际分数(因为37.30在浮点数中是37.3，需要乘以100得到30)
    # 先转换为字符串来准确提取小数部分
    str_value = f"{degree_minute:.10f}"  # 转换为字符串保留足够精度
    if '.' in str_value:
        whole_part, decimal_part = str_value.split('.')
        # 补齐小数部分到6位，然后取前4位作为分的整数和小数部分
        decimal_part = decimal_part.ljust(6, '0')[:4]
        minutes = float(decimal_part) / 100  # 将分的数值转换为实际数值
    else:
        minutes = 0.0

    # 转换为十进制度
    decimal_degrees = degrees + minutes / 60
    return round(decimal_degrees, 6)


def convert_coord_dict(coord_dict):
    """
    转换整个坐标字典
    """
    converted_dict = {}

    for city, data in coord_dict.items():
        converted_dict[city] = {
            "range": {
                "latitude": [dm_to_decimal(data["range"]["latitude"][0]),
                             dm_to_decimal(data["range"]["latitude"][1])],
                "longitude": [dm_to_decimal(data["range"]["longitude"][0]),
                              dm_to_decimal(data["range"]["longitude"][1])]
            },
            "center": {
                "latitude": dm_to_decimal(data["center"]["latitude"]),
                "longitude": dm_to_decimal(data["center"]["longitude"])
            }
        }

    return converted_dict


def print_converted_data(converted_dict):
    """
    打印转换后的数据，便于查看
    """
    print("转换后的经纬度数据（十进制度）：")
    print("=" * 60)

    for city, data in converted_dict.items():
        print(f"\n{city}:")
        print(f"  纬度范围: [{data['range']['latitude'][0]:.6f}, {data['range']['latitude'][1]:.6f}]")
        print(f"  经度范围: [{data['range']['longitude'][0]:.6f}, {data['range']['longitude'][1]:.6f}]")
        print(f"  中心点: 纬度={data['center']['latitude']:.6f}, 经度={data['center']['longitude']:.6f}")


# 您的原始数据
Longitude_latitude = {
    "银川": {"range": {"latitude": [37.29, 38.52], "longitude": [105.48, 106.52]},
             "center": {"latitude": 38.29, "longitude": 106.13}},
    "石嘴山": {"range": {"latitude": [38.21, 39.25], "longitude": [105.58, 106.39]},
               "center": {"latitude": 39.02, "longitude": 106.22}},
    "吴忠": {"range": {"latitude": [36.34, 38.15], "longitude": [105.7, 107.47]},
             "center": {"latitude": 37.59, "longitude": 106.11}},
    "固原": {"range": {"latitude": [35.14, 36.31], "longitude": [105.19, 106.57]},
             "center": {"latitude": 36.00, "longitude": 106.15}},
    "中卫": {"range": {"latitude": [36.06, 37.50], "longitude": [104.17, 106.10]},
             "center": {"latitude": 37.30, "longitude": 105.11}},
}

Longitude_latitude10 = {
    "银川": {"range": {"latitude": [37.48, 38.87], "longitude": [105.80, 106.87]},
             "center": {"latitude": 38.48, "longitude": 106.22}},
    "石嘴山": {"range": {"latitude": [38.35, 39.42], "longitude": [105.97, 106.65]},
               "center": {"latitude": 39.03, "longitude": 106.22}},
    "吴忠": {"range": {"latitude": [36.56, 38.25], "longitude": [106.17, 107.78]},
             "center": {"latitude": 37.98, "longitude": 106.18}},
    "固原": {"range": {"latitude": [35.23, 36.52], "longitude": [105.32, 106.95]},
             "center": {"latitude": 36.00, "longitude": 106.25}},
    "中卫": {"range": {"latitude": [36.10, 37.83], "longitude": [104.28, 106.17]},
             "center": {"latitude": 37.50, "longitude": 105.18}},
}

# 执行转换
if __name__ == "__main__":
    # 转换数据
    converted_data = convert_coord_dict(Longitude_latitude)

    # 打印结果
    print_converted_data(converted_data)

    # 同时输出可直接使用的字典格式
    print("\n" + "=" * 60)
    print("可直接复制的字典格式：")
    print("converted_coordinates = {")
    for city, data in converted_data.items():
        lat_range = [round(data['range']['latitude'][0], 6), round(data['range']['latitude'][1], 6)]
        lon_range = [round(data['range']['longitude'][0], 6), round(data['range']['longitude'][1], 6)]
        center_lat = round(data['center']['latitude'], 6)
        center_lon = round(data['center']['longitude'], 6)

        print(f'"{city}": {{"range": {{"latitude": {lat_range}, "longitude": {lon_range}}}, ')
        print(f'"center": {{"latitude": {center_lat}, "longitude": {center_lon}}},')
    print("}")