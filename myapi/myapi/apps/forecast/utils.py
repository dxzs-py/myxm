import os
import numpy as np
from django.conf import settings
from .data_loader import WeatherDataLoader
from .predictors.transformer_lstm import TransformerLSTM
import pandas as pd


class PredictionService:
    def __init__(self, target_indices):
        self.config = {
            'input_window': 60,
            'output_window': 15,
            'target_indices': target_indices,
            'model_class': TransformerLSTM,
            'model_path': os.path.join(
                settings.BASE_DIR, 'apps', 'forecast', 'static', f'best_model_{target_indices}.pth'
            )
        }
        self.data_loader = WeatherDataLoader()
        self.model = self._load_model()

    def _load_model(self):
        # 获取数据以确定特征数量
        processed_data, _, feature_names = self.data_loader.load_and_preprocess()
        num_features = processed_data.shape[1]

        # 创建模型实例
        model = self.config['model_class'](
            input_window=self.config['input_window'],
            output_window=self.config['output_window'],
            target_indices=self.config['target_indices'],
            num_features=num_features
        )

        # 加载预训练权重
        model.load_weights(self.config['model_path'])
        return model

    def make_prediction(self, time_difference=0):
        """执行预测并返回结果"""
        # 获取最新输入序列
        input_sequence = self.data_loader.get_now_sequence(self.config['input_window'], time_difference=time_difference,
                                                           use_processed=True)

        # 执行预测
        predictions = self.model.predict(input_sequence)

        # 反归一化结果

        feature_name = self.data_loader.feature_names[self.config['target_indices']]
        pred_values = self.inverse_transform(predictions[0, :], self.config['target_indices'])
        results = {
            'feature_name': feature_name,
            'values': pred_values.tolist()
        }

        return results

    def inverse_transform(self, data, feature_idx):
        """反归一化单个特征"""
        if self.data_loader.scaler is None:
            self.data_loader.load_and_preprocess()

        orig_shape = data.shape
        data = data.reshape(-1)
        n_features = self.data_loader.scaler.n_features_in_
        dummy = np.zeros((len(data), n_features))
        dummy[:, feature_idx] = data

        # 应用逆变换
        result = np.zeros_like(dummy)
        for name, transformer, columns in self.data_loader.scaler.transformers_:
            if name != 'remainder':
                col_data = dummy[:, columns]
                if hasattr(transformer, 'inverse_transform'):
                    inv_data = transformer.inverse_transform(col_data)
                else:
                    inv_data = col_data
                result[:, columns] = inv_data

        # 处理remainder列
        if self.data_loader.scaler.remainder != 'drop':
            remainder_cols = [i for i in range(n_features)
                              if not any(i in columns for _, _, columns in self.data_loader.scaler.transformers_[:-1])]
            if remainder_cols:
                result[:, remainder_cols] = dummy[:, remainder_cols]

        return result[:, feature_idx].reshape(-1)


class NingxiaDisasterIdentifier:
    def __init__(self):
        # 宁夏地区特定阈值参数
        self.params = {
            # 沙尘暴参数
            'sandstorm': {
                'wind_thresholds': [10, 15, 20],  # 轻度, 中度, 重度风速阈值(m/s)
                'humidity_threshold': 40,  # 最大湿度阈值(%)
                'dry_days_threshold': 5,  # 干旱天数阈值
                'precip_threshold': 5  # 3天累计降水阈值(mm)
            },

            # 冰雹参数
            'hail': {
                'precip_threshold': 10,  # 降水阈值(mm)
                'temp_change_threshold': 0.5,  # 温度变化率阈值(℃/h)
                'temp_range_threshold': 12,  # 日温差阈值(℃)
                'humidity_drop_threshold': 20,  # 湿度下降阈值(%)
                'convection_thresholds': [50, 100]  # 对流指数阈值
            },

            # 暴雨参数
            'rainstorm': {
                'thresholds': [30, 50, 70, 100]  # 轻, 中, 重, 特重阈值(mm)
            },

            # 霜冻参数
            'frost': {
                'temp_thresholds': [0, -2, -5],  # 轻, 中, 重温度阈值(℃)
                'sensitive_months': [3, 4, 9, 10]  # 敏感月份
            },

            # 高温参数
            'heat': {
                'temp_thresholds': [35, 37, 40],  # 轻, 中, 重温度阈值(℃)
                'duration_thresholds': [3, 5]  # 持续天数阈值
            },

            # 极端低温参数
            'extreme_low': {
                'temp_thresholds': [-5, -10, -15],  # 轻, 中, 重温度阈值(℃)
                'deviation_thresholds': [5, 7, 10]  # 温度偏离阈值
            }
        }

    def identify_sandstorm(self, data, prev_days):
        """
        沙尘暴识别 - 考虑风速、湿度、干旱持续时间和前期降水
        参数:
            data: 当日数据Series
            prev_days: 前几天的DataFrame
        返回:
            沙尘暴等级
        """
        p = self.params['sandstorm']

        # 计算干旱持续天数
        dry_days = (prev_days['降水量（mm）'] < 1).sum()

        # 计算3天累计降水
        precip_3d = prev_days.head(3)['降水量（mm）'].sum()

        # 风速是主要指标
        wind_speed = data['10m平均风速（m/s）']

        # 湿度条件
        humidity = data['相对湿度（%）']

        # 综合判断
        if (wind_speed >= p['wind_thresholds'][0] and
                humidity <= p['humidity_threshold'] and
                dry_days >= p['dry_days_threshold'] and
                precip_3d <= p['precip_threshold']):

            if wind_speed >= p['wind_thresholds'][2]:
                return "沙尘暴-特强级"
            elif wind_speed >= p['wind_thresholds'][1]:
                return "沙尘暴-重度"
            elif wind_speed >= p['wind_thresholds'][0]:
                return "沙尘暴-中度"

        return "无沙尘暴"

    def identify_hail(self, data, prev_day):
        """
        冰雹识别 - 结合降水、温度变化、湿度变化和日温差
        参数:
            data: 当日数据Series
            prev_day: 前一天数据Series
        返回:
            冰雹等级
        """
        p = self.params['hail']

        # 基本条件检查
        if data['降水量（mm）'] < p['precip_threshold']:
            return "无冰雹"

        # 计算温度变化率 (℃/h)
        temp_change_rate = abs(data['平均气温（℃）'] - prev_day['平均气温（℃）']) / 24

        # 计算日温差
        daily_temp_range = data['最高气温（℃）'] - data['最低气温（℃）']

        # 计算湿度下降
        humidity_drop = prev_day['相对湿度（%）'] - data['相对湿度（%）']

        # 计算对流指数
        convection_index = (data['降水量（mm）'] *
                            temp_change_rate *
                            (daily_temp_range / 10) *
                            max(1, humidity_drop / 10))

        # 综合判断
        if (temp_change_rate >= p['temp_change_threshold'] and
                daily_temp_range >= p['temp_range_threshold'] and
                humidity_drop >= p['humidity_drop_threshold']):

            if convection_index >= p['convection_thresholds'][1]:
                return "冰雹-重度"
            elif convection_index >= p['convection_thresholds'][0]:
                return "冰雹-中度"
            else:
                return "冰雹-轻度"

        return "无冰雹"

    def identify_rainstorm(self, precipitation):
        """
        暴雨识别
        参数:
            precipitation: 日降水量(mm)
        返回:
            暴雨等级
        """
        p = self.params['rainstorm']['thresholds']

        if precipitation >= p[3]:
            return "暴雨-红色特重级"
        elif precipitation >= p[2]:
            return "暴雨-橙色重度"
        elif precipitation >= p[1]:
            return "暴雨-黄色中度"
        elif precipitation >= p[0]:
            return "暴雨-蓝色轻度"
        else:
            return "无暴雨"

    def identify_frost(self, data, month):
        """
        霜冻识别 - 考虑温度、月份和日照
        参数:
            data: 当日数据Series
            month: 当前月份
        返回:
            霜冻等级
        """
        p = self.params['frost']

        # 只在敏感月份检测
        if month not in p['sensitive_months']:
            return "无霜冻"

        min_temp = data['最低气温（℃）']

        # 日照条件：日照少时霜冻更易发生
        sunshine_factor = max(0, 1 - data['日照时数（小时）'] / 10)

        # 湿度条件：湿度高时霜冻影响更大
        humidity_factor = min(1, data['相对湿度（%）'] / 80)

        # 综合影响因子
        frost_factor = sunshine_factor * humidity_factor

        # 调整温度阈值
        adj_temp_thresholds = [t * (1 + frost_factor) for t in p['temp_thresholds']]

        if min_temp <= adj_temp_thresholds[2]:
            return "霜冻-重度"
        elif min_temp <= adj_temp_thresholds[1]:
            return "霜冻-中度"
        elif min_temp <= adj_temp_thresholds[0]:
            return "霜冻-轻度"

        return "无霜冻"

    def identify_extreme_heat(self, data, heat_days):
        """
        极端高温识别 - 考虑温度、持续时间和湿度
        参数:
            data: 当日数据Series
            heat_days: 连续高温天数
        返回:
            高温等级
        """
        p = self.params['heat']
        max_temp = data['最高气温（℃）']

        # 湿度影响：湿度高时体感温度更高
        humidity_factor = min(1.2, 1 + (data['相对湿度（%）'] - 50) / 100)

        # 风速影响：风速低时体感温度更高
        wind_factor = min(1.2, 1 + (5 - min(data['10m平均风速（m/s）'], 5)) / 10)

        # 计算体感温度
        felt_temp = max_temp * humidity_factor * wind_factor

        # 高温分级
        if felt_temp >= p['temp_thresholds'][2] or (
                felt_temp >= p['temp_thresholds'][1] and heat_days >= p['duration_thresholds'][1]):
            return "高温-红色重级"
        elif felt_temp >= p['temp_thresholds'][1] or (
                felt_temp >= p['temp_thresholds'][0] and heat_days >= p['duration_thresholds'][0]):
            return "高温-橙色中级"
        elif felt_temp >= p['temp_thresholds'][0]:
            return "高温-黄色轻度"

        return "无高温"

    def identify_extreme_low_temp(self, data, prev_days):
        """
        极端低温识别 - 考虑温度、变化率和历史对比
        参数:
            data: 当日数据Series
            prev_days: 前几天DataFrame
        返回:
            低温等级
        """
        p = self.params['extreme_low']
        min_temp = data['最低气温（℃）']

        # 计算温度变化率
        temp_change_rate = (min_temp - prev_days.iloc[0]['最低气温（℃）']) / 24

        # 计算近期低温平均值
        avg_low_temp = prev_days.head(7)['最低气温（℃）'].mean()

        # 低温偏离度
        deviation = avg_low_temp - min_temp

        # 分级标准
        if min_temp <= p['temp_thresholds'][2] or deviation >= p['deviation_thresholds'][2]:
            return "极端低温-红色重级"
        elif min_temp <= p['temp_thresholds'][1] or deviation >= p['deviation_thresholds'][1]:
            return "极端低温-橙色中级"
        elif min_temp <= p['temp_thresholds'][0] or deviation >= p['deviation_thresholds'][0]:
            return "极端低温-黄色轻度"

        return "无极端低温"

    def calculate_heat_days(self, data, prev_days):
        """
        计算连续高温天数
        参数:
            data: 当日数据Series
            prev_days: 前几天DataFrame
        返回:
            连续高温天数
        """
        heat_days = 0
        threshold = self.params['heat']['temp_thresholds'][0]

        # 检查当天
        if data['最高气温（℃）'] >= threshold:
            heat_days += 1

            # 检查历史天数（按日期倒序）
            for i in range(len(prev_days)):
                if prev_days.iloc[i]['最高气温（℃）'] >= threshold:
                    heat_days += 1
                else:
                    break

        return heat_days

    def identify_all(self, data, prev_days):
        """
        综合识别所有灾害
        参数:
            data: 当日数据Series
            prev_days: 前几天DataFrame(至少7天)
        返回:
            灾害识别结果字典
        """
        # 确保有足够的历史数据
        if len(prev_days) < 7:
            raise ValueError("至少需要7天的历史数据")

        # 计算连续高温天数
        heat_days = self.calculate_heat_days(data, prev_days)

        # 灾害识别
        results = {
            '暴雨': self.identify_rainstorm(data['降水量（mm）']),
            '沙尘暴': self.identify_sandstorm(data, prev_days),
            '冰雹': self.identify_hail(data, prev_days.iloc[0]),
            '霜冻': self.identify_frost(data, data['月份']),
            '高温': self.identify_extreme_heat(data, heat_days),
            '极端低温': self.identify_extreme_low_temp(data, prev_days)
        }

        return results


# 示例使用
if __name__ == "__main__":
    # 创建识别器实例
    identifier = NingxiaDisasterIdentifier()

    # 创建DataFrame数据
    # prev_days = pd.DataFrame([
    #     # 第7天前 (最早)
    #     {'年份': 2025, '月份': 4, '日': 8, '最高气温（℃）': 30.0, '最低气温（℃）': 12.0, '平均气温（℃）': 18.0,
    #      '10m平均风速（m/s）': 6.5, '日照时数（小时）': 6.0, '相对湿度（%）': 60, '降水量（mm）': 0},
    #     # 第6天前
    #     {'年份': 2025, '月份': 4, '日': 9, '最高气温（℃）': 31.0, '最低气温（℃）': 11.0, '平均气温（℃）': 18.5,
    #      '10m平均风速（m/s）': 7.0, '日照时数（小时）': 6.5, '相对湿度（%）': 55, '降水量（mm）': 0},
    #     # 第5天前
    #     {'年份': 2025, '月份': 4, '日': 10, '最高气温（℃）': 32.0, '最低气温（℃）': 10.0, '平均气温（℃）': 19.0,
    #      '10m平均风速（m/s）': 7.5, '日照时数（小时）': 7.0, '相对湿度（%）': 50, '降水量（mm）': 0},
    #     # 第4天前
    #     {'年份': 2025, '月份': 4, '日': 11, '最高气温（℃）': 33.0, '最低气温（℃）': 9.0, '平均气温（℃）': 19.5,
    #      '10m平均风速（m/s）': 8.0, '日照时数（小时）': 7.5, '相对湿度（%）': 45, '降水量（mm）': 0},
    #     # 第3天前
    #     {'年份': 2025, '月份': 4, '日': 12, '最高气温（℃）': 34.0, '最低气温（℃）': 8.0, '平均气温（℃）': 20.0,
    #      '10m平均风速（m/s）': 9.0, '日照时数（小时）': 8.0, '相对湿度（%）': 40, '降水量（mm）': 0},
    #     # 第2天前
    #     {'年份': 2025, '月份': 4, '日': 13, '最高气温（℃）': 35.5, '最低气温（℃）': 7.0, '平均气温（℃）': 20.5,
    #      '10m平均风速（m/s）': 10.5, '日照时数（小时）': 8.5, '相对湿度（%）': 35, '降水量（mm）': 0},
    #     # 第1天前 (最近)
    #     {'年份': 2025, '月份': 4, '日': 14, '最高气温（℃）': 36.0, '最低气温（℃）': 6.0, '平均气温（℃）': 21.0,
    #      '10m平均风速（m/s）': 12.0, '日照时数（小时）': 9.0, '相对湿度（%）': 30, '降水量（mm）': 0},
    #     # 当天数据
    #     {'年份': 2025, '月份': 4, '日': 15, '最高气温（℃）': 38.5, '最低气温（℃）': 5.2, '平均气温（℃）': 22.0,
    #      '10m平均风速（m/s）': 18.2, '日照时数（小时）': 8.5, '相对湿度（%）': 25, '降水量（mm）': 12.0},
    # ])

    prev_days = pd.read_csv('static/data_finally.csv').iloc[-8:]
    # 分离当天数据和历史数据
    today = prev_days.iloc[-1]  # 当天数据
    prev_days = prev_days.iloc[:-1]  # 历史数据

    # 灾害识别
    disasters = identifier.identify_all(today, prev_days)

    print("宁夏气象灾害识别结果:")
    for disaster, level in disasters.items():
        print(f"{disaster}: {level}")
