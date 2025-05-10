import math

import torch
import torch.nn as nn


class BasePredictor(nn.Module):
    def __init__(self, input_window, output_window, target_indices, num_features):
        super().__init__()
        self.input_window = input_window
        self.output_window = output_window
        self.target_indices = target_indices
        self.num_features = num_features

    def predict(self, input_data):
        """执行预测并返回结果"""
        raise NotImplementedError("子类必须实现此方法")

    def load_weights(self, model_path, device=None):
        """加载预训练权重"""
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_state_dict(torch.load(model_path, map_location=device))
        self.to(device)
        self.eval()

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.2, max_len=60):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe = torch.zeros(1, max_len, d_model)
        pe[0, :, 0::2] = torch.sin(position * div_term)
        pe[0, :, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1)]
        return self.dropout(x)

