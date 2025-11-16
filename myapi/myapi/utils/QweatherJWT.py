from typing import Dict
from myapi.settings.constants import SIGNATURE, PROOF_ID, SUB
import jwt
import time


class QWeatherJWTAuth:
    """和风天气JWT认证工具类"""

    def __init__(self, proof_id: str = PROOF_ID, private_key: str = SIGNATURE, sub: str = SUB):
        """
        初始化JWT认证
        Args:
            proof_id: 和风天气分配的公钥ID
            private_key: 和风天气分配的私钥
        """
        self.proof_id = proof_id
        self.private_key = private_key
        self.sub = sub

    def generate_token(self, expiration_minutes: int = 15) -> str:
        """
        生成JWT令牌
        Args:
            expiration_minutes: 令牌有效期（分钟）
        Returns:
            JWT令牌字符串
        """
        # 当前时间戳
        now = int(time.time()) - 30
        exp = now + (expiration_minutes * 60) + 30

        # 创建JWT头部
        headers = {
            "alg": "EdDSA",
            "kid": self.proof_id
        }

        # 创建JWT载荷
        payload = {
            "sub": self.sub,  # 主题
            "iat": now,  # 签发时间
            "exp": exp,  # 过期时间
        }

        jwt_token = jwt.encode(payload, self.private_key, algorithm='EdDSA', headers=headers)
        return jwt_token

    def get_auth_headers(self, token: str = None) -> Dict[str, str]:
        """获取认证请求头"""
        if token is None:
            token = self.generate_token()
        return {"Authorization": f"Bearer {token}"}


if __name__ == '__main__':
    auth = QWeatherJWTAuth()
    token = auth.generate_token()
    print(token)


