from calendar import month

import pandas as pd
import numpy as np
import os
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, RobustScaler
from django.conf import settings
from datetime import datetime, timedelta

from sympy.physics.units import years

from myapi.settings.constants import BEIJING_TZ, POSTPONE_THE_YEAR


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
        """
        使用 rename 方法将这些列重命名为标准的英文名称 'year', 'month', 'day' 
        使用 pd.to_datetime() 函数将这三列数据转换为 pandas 的 datetime 类型对象
        当使用 pd.to_datetime() 函数并传入包含年、月、日信息的 DataFrame 时，pandas 要求这些列必须有标准的英文名称（'year', 'month', 'day'），这样它才能正确识别每一列的含义。
        """

        df['day_of_year'] = dates.dt.dayofyear
        """
        .dt 是访问日期时间属性的访问器，通过它可以访问 datetime 对象的各种属性
        .dayofyear 是 dt 访问器提供的一个属性，用于获取日期对应的一年中的第几天（1-366）
        dt 访问器还提供了很多其他有用的日期时间属性和方法，比如 .year、.month、.day、.hour、.minute、.second 等用于获取具体时间部分，以及 .weekday()、.quarter 等用于获取其他日期相关信息的方法。
        """
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
        self.scaler = ColumnTransformer(transformers, remainder='passthrough')  # 表示未在任何转换器中指定的列将被保留原样
        """
        ColumnTransformer 是 sklearn 提供的一个用于对不同列进行不同预处理的工具。它可以将多个不同的预处理步骤（如缩放、标准化、编码等）应用到不同的列上，最后将这些处理后的列合并起来。
        每个转换器都是一个元组，包含三个元素：
        转换器的名称（用于标识该转换器）
        转换器对象（如 MinMaxScaler、RobustScaler 等）
        要应用该转换器的列的索引列表或名称列表
        允许为不同列应用不同的转换方法
        保持所有特征的原始顺序
        便于集成到机器学习工作流中
        remainder='passthrough' 表示未在任何转换器中指定的列将被保留原样，不进行任何处理。
        """

        self.processed_data = self.scaler.fit_transform(df.values)
        return self.processed_data, self.scaler, self.feature_names

    def get_now_sequence(self, input_size, time_difference, use_processed=False, future=False):
        if self.processed_data is None:
            self.load_and_preprocess()

        if future:
            end_idx = - time_difference + input_size if time_difference > 0 else None
            start_idx = -time_difference if time_difference > 0 else -input_size
        else:
            end_idx = -time_difference if time_difference > 0 else None
            start_idx = -input_size - time_difference if time_difference > 0 else -input_size

        if use_processed:
            return self.processed_data[start_idx:end_idx]
        else:
            return self.raw_data.iloc[start_idx:end_idx]

    def get_now_date(self):
        if self.raw_data is None:
            self.load_and_preprocess()
        # 获取东八区当前时间
        now_date = datetime.now(BEIJING_TZ)
        now_date = datetime(now_date.year - POSTPONE_THE_YEAR, now_date.month, now_date.day, tzinfo=BEIJING_TZ)
        years = int(self.raw_data.iloc[-1]['年份'])
        month = int(self.raw_data.iloc[-1]['月份'])
        day = int(self.raw_data.iloc[-1]['日'])
        time_difference = abs(now_date - datetime(years, month, day, tzinfo=BEIJING_TZ)).days

        return {
            'year': now_date.year,
            'month': now_date.month,
            'day': now_date.day,
            'time_difference': time_difference
        }
