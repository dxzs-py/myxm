import pandas as pd
import numpy as np
import os
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, RobustScaler
from django.conf import settings


class WeatherDataLoader:
    def __init__(self, file_path=None):
        self.file_path = file_path or os.path.join(
            settings.BASE_DIR, 'apps', 'forecast', 'static', 'data_finally.csv'
        )
        self.scaler = None
        self.feature_names = None
        self.raw_data = None
        self.processed_data = None

    def load_and_preprocess(self):
        df = pd.read_csv(self.file_path)
        self.raw_data = df.copy()

        # 提取时间列并转换为周期性特征
        year_cols = [col for col in df.columns if "年份" in col]
        month_cols = [col for col in df.columns if "月份" in col]
        day_cols = [col for col in df.columns if "日" in col]

        if not year_cols or not month_cols or not day_cols:
            raise ValueError("无法找到时间列（年份、月份、日）")

        year_col = year_cols[0]
        month_col = month_cols[0]
        day_col = day_cols[0]

        # 计算一年中的第几天
        dates = pd.to_datetime(df[[year_col, month_col, day_col]].rename(columns={
            year_col: 'year', month_col: 'month', day_col: 'day'
        }))
        df['day_of_year'] = dates.dt.dayofyear
        df['day_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365.25)
        df['day_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365.25)

        # 删除原始时间列
        df = df.drop([year_col, month_col, day_col, 'day_of_year'], axis=1)
        self.feature_names = df.columns.tolist()

        # 自动识别不同类型的列
        temp_cols = [i for i, col in enumerate(self.feature_names) if '气温' in col]
        other_cols = [i for i, col in enumerate(self.feature_names) if i not in temp_cols]

        sun_col = None
        humid_col = None
        wind_col = None

        for i, col in enumerate(self.feature_names):
            if '日照时数' in col:
                sun_col = i
            elif '相对湿度' in col:
                humid_col = i
            elif '风速' in col:
                wind_col = i

        # 构建预处理管道
        transformers = []
        if temp_cols:
            transformers.append(('temp', MinMaxScaler(feature_range=(-1, 1)), temp_cols))
        if sun_col is not None:
            transformers.append(('sun', RobustScaler(), [sun_col]))
        if humid_col is not None:
            transformers.append(('humid', MinMaxScaler(feature_range=(0, 1)), [humid_col]))
        if wind_col is not None:
            transformers.append(('wind', RobustScaler(), [wind_col]))
        if other_cols:
            transformers.append(('other', MinMaxScaler(feature_range=(-1, 1)), other_cols))

        # 创建ColumnTransformer
        self.scaler = ColumnTransformer(transformers, remainder='passthrough')
        self.processed_data = self.scaler.fit_transform(df.values)
        return self.processed_data, self.scaler, self.feature_names

    def get_latest_sequence(self, input_size):
        if self.processed_data is None:
            self.load_and_preprocess()
        return self.processed_data[-input_size:]

    def get_last_date(self):
        if self.raw_data is None:
            self.load_and_preprocess()

        year_col = [col for col in self.raw_data.columns if "年份" in col][0]
        month_col = [col for col in self.raw_data.columns if "月份" in col][0]
        day_col = [col for col in self.raw_data.columns if "日" in col][0]

        return {
            'year': int(self.raw_data[year_col].iloc[-1]),
            'month': int(self.raw_data[month_col].iloc[-1]),
            'day': int(self.raw_data[day_col].iloc[-1])
        }