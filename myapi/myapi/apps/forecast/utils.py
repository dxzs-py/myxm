import os
import numpy as np
from django.conf import settings
from .data_loader import WeatherDataLoader
from .predictors.transformer_lstm import TransformerLSTM


class PredictionService:
    def __init__(self,target_indices):
        self.config = {
            'input_window': 60,
            'output_window': 15,
            'target_indices': target_indices,
            'model_class': TransformerLSTM,
            'model_path': os.path.join(
                settings.BASE_DIR,  'apps', 'forecast', 'static', f'best_model_{target_indices}.pth'
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

    def make_prediction(self):
        """执行预测并返回结果"""
        # 获取最新输入序列
        input_sequence = self.data_loader.get_latest_sequence(self.config['input_window'])

        # 执行预测
        predictions = self.model.predict(input_sequence)

        # 反归一化结果

        feature_name = self.data_loader.feature_names[self.config['target_indices']]
        pred_values = self.inverse_transform(predictions[0, :], self.config['target_indices'])
        results={
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