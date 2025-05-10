import torch
import torch.nn as nn
import math
from .base import BasePredictor,PositionalEncoding



# 位置编码和混合损失类保持不变

class TransformerLSTM(BasePredictor):
    def __init__(self, input_window, output_window, target_indices, num_features,
                 lstm_hidden_dim=64, transformer_dim=64, num_transformer_layers=2):
        super().__init__(input_window, output_window, target_indices, num_features)

        # LSTM 分支
        self.lstm = nn.LSTM(
            input_size=num_features,
            hidden_size=lstm_hidden_dim,
            num_layers=2,
            batch_first=True,
            bidirectional=True
        )

        # Transformer 分支
        self.input_proj = nn.Linear(num_features, transformer_dim)
        self.pos_encoder = PositionalEncoding(transformer_dim, dropout=0.15)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=transformer_dim,
            nhead=4,
            dim_feedforward=256,
            dropout=0.15,
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_transformer_layers
        )

        # 特征融合
        self.fusion = nn.Sequential(
            nn.Linear(lstm_hidden_dim * 2 + transformer_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.15)
        )

        # 输出层
        self.output_layer = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)  # 我一个模型预测一个特征
        )

    def forward(self, x):
        # LSTM 分支
        lstm_out, _ = self.lstm(x)
        lstm_feature = lstm_out[:, -self.output_window:, :]

        # Transformer 分支
        x_proj = self.input_proj(x)
        x_pos = self.pos_encoder(x_proj)
        trans_out = self.transformer_encoder(x_pos)
        trans_feature = trans_out[:, -self.output_window:, :]

        # 特征融合
        combined = torch.cat([lstm_feature, trans_feature], dim=-1)
        fused = self.fusion(combined)

        # 预测所有时间步
        outputs = self.output_layer(fused)
        return outputs

    def predict(self, input_data):
        """执行预测"""
        device = next(self.parameters()).device
        with torch.no_grad():
            input_tensor = torch.FloatTensor(input_data).unsqueeze(0).to(device)
            output = self(input_tensor)
            return output.cpu().numpy()