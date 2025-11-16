import logging
from functools import lru_cache
from myapi.utils.QweatherJWT import QWeatherJWTAuth
import requests
from typing import Dict, List

# 假设 QWEATHER_KEY 已定义在项目配置中
from myapi.settings.constants import QWEATHER_KEY, API_HOST, URGENCY, SEVERITY, CERTAINTY

logger = logging.getLogger(__name__)

address_id = {
    "银川": "101170101",
    "吴忠": "101170301",
    "固原": "101170401",
    "中卫": "101170501",
    "石嘴山": "101170201",

}

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


# ========== 异常定义 ==========
class WeatherServiceException(Exception):
    """天气服务基类异常"""
    pass


class GeocodeError(WeatherServiceException):
    """地理编码失败"""
    pass


class WeatherBaseError(WeatherServiceException):
    """获取当前天气失败"""
    pass


class WeatherForecastError(WeatherServiceException):
    """获取预报信息失败"""
    pass


class WeatherAlertError(WeatherServiceException):
    """获取天气预警失败"""
    pass


# ========== 天气服务主类 ==========
class QWeatherService:
    def __init__(self, address: str):
        self.address = address
        self.jwt = QWeatherJWTAuth().get_auth_headers()
        self.key = QWEATHER_KEY
        self.api_host = API_HOST
        self.location_id = self._get_location_id()
        self.now_info = self._get_weather_now()
        self.alert = self._get_weather_alert()

    # 获取api信息
    @lru_cache(maxsize=128)
    def _get_location_id(self) -> str:
        """获取地理位置ID"""
        if self.address in address_id:
            return address_id[self.address]
        # 如果以后要拓展地图就这样但是就是有点浪费资源
        url = f"https://{self.api_host}/geo/v2/city/lookup/?location={self.address}&amd=银川"
        try:
            response = requests.get(url, headers=self.jwt)
        except requests.RequestException as e:
            logger.error("地理编码请求失败", exc_info=True)
            raise GeocodeError(f"网络请求失败：{e}") from e

        if response.status_code != 200:
            logger.warning("地理编码API返回非200状态码：%s", response.status_code)
            raise GeocodeError("地理编码API请求失败")
        data = response.json()
        if not data.get("location"):
            logger.warning("未获取到地理位置数据：%s", data)
            raise GeocodeError("未获取到地理位置数据")

        for loc in data["location"]:
            if loc["name"] == self.address:
                return loc["id"]

        logger.warning("未找到匹配的地址ID：%s", self.address)
        raise GeocodeError(f"未找到对应的城市ID：{self.address}")

    def _get_weather_now(self) -> Dict:
        url = f"https://{self.api_host}/v7/weather/now?location={self.location_id}"

        try:
            response = requests.get(url, headers=self.jwt)
        except requests.RequestException as e:
            logger.error("实时天气信息请求失败", exc_info=True)
            raise WeatherBaseError(f"网络请求失败：{e}") from e

        if response.status_code != 200:
            logger.warning("实时天气API返回非200状态码：%s", response.status_code)
            raise WeatherBaseError("实时天气信息请求失败")

        data = response.json()
        if not data.get("now"):
            logger.warning("未获取到实时天气数据：%s", data)
            raise WeatherBaseError("未获取到实时天气数据")

        return data["now"]

    def _get_weather_forecast(self, days: int = 3) -> List[Dict]:
        url = f"https://{self.api_host}/v7/weather/{days}d?location={self.location_id}&days=3"

        try:
            response = requests.get(url, headers=self.jwt)
        except requests.RequestException as e:
            logger.error("天气预报信息请求失败", exc_info=True)
            raise WeatherForecastError(f"网络请求失败：{e}") from e

        if response.status_code != 200:
            logger.warning("天气预报API返回非200状态码：%s", response.status_code)
            raise WeatherForecastError("天气预报信息请求失败")

        data = response.json()
        if not data.get("daily"):
            logger.warning("未获取到天气预报数据：%s", data)
            raise WeatherForecastError("未获取到天气预报数据")

        return data["daily"]

    def _get_weather_alert(self) -> Dict:
        url = f"https://{self.api_host}/weatheralert/v1/current/{Longitude_latitude10[self.address]['center']['latitude']}/{Longitude_latitude10[self.address]['center']['longitude']}"
        # url = f"https://{self.api_host}/v7/warning/now?location={self.location_id}"
        try:
            response = requests.get(url, headers=self.jwt)
        except requests.RequestException as e:
            logger.error("天气预警信息请求失败", exc_info=True)
            raise WeatherAlertError(f"网络请求失败：{e}") from e

        if response.status_code != 200:
            logger.warning("天气预警API返回非200状态码：%s", response.status_code)
            raise WeatherAlertError("天气预警信息请求失败")

        data = response.json()
        # 没有预警信息时，warning字段可能为空列表，这是正常情况
        return data

    # 输出格式化的天气预警信息

    def get_weather_alert(self) :
        """获取格式化的天气预警信息"""
        try:
            if self.alert["metadata"]["zeroResult"] is True:
                return None
            else:
                warnings = []
                for alert in self.alert["alerts"]:
                    warnings.append({
                        "eventType": alert["eventType"]["name"],
                        "urgency": "并不紧急" if alert["urgency"] is None else URGENCY[alert["urgency"]],
                        "severity ": SEVERITY[alert["severity"]],
                        "certainty": "100%" if alert["certainty"] is None else CERTAINTY[alert["certainty"]],
                        "icon": alert["icon"],
                        "color":alert["color"],
                        "expireTime":alert["expireTime"],
                        "headline":alert["headline"],
                        "description": alert["description"],
                        "criteria":alert["criteria"],
                        "instruction ":alert["instruction"],
                        "responseTypes":alert["responseTypes"],
                    })
                return  warnings
        except KeyError:
            logger.warning("天气预警数据结构异常：%s", self.alert)
            return "天气预警数据结构异常"

    def get_current_weather(self) -> Dict:
        return {
            "city": self.address,
            "temperature": self.now_info["temp"],
            "feels_like": self.now_info["feelsLike"],
            "weather": self.now_info["text"],
            "humidity": self.now_info["humidity"],
            "precipitation": self.now_info["precip"],  # 降水量
            "pressure": self.now_info["pressure"],  # 气压
            "windspeed": self.now_info["windSpeed"],
        }

    def get_forecast_weather(self, days: int = 3) -> List[Dict]:
        forecasts = []
        for day in self._get_weather_forecast(days):
            forecasts.append({
                "city": self.address,
                "date": day["fxDate"],
                "temp_max": float(day["tempMax"]),
                "temp_min": float(day["tempMin"]),
                "precip ": day["precip"],
                "sunset": day["sunset"],
                "windSpeedDay": day["windSpeedDay"],
                "windSpeedNight": day["windSpeedNight"],
                "humidity": day["humidity"],
                "pressure": day["pressure"],
            })
        return forecasts

    @staticmethod
    def get_weather_info(address: str, choose: int = 3, days: int = 3) -> dict:
        try:
            instance = QWeatherService(address)
            data = {}
            if choose == 1:
                data["current"] = instance.get_current_weather()
            elif choose == 2:
                data["forecast"] = instance.get_forecast_weather(days)
            elif choose == 4:
                data["alert"] = instance.get_weather_alert()
            else:
                data["current"] = instance.get_current_weather()
                data["forecast"] = instance.get_forecast_weather(days)
                data["alert"] = instance.get_weather_alert()

            return data
        except WeatherServiceException as e:
            logger.error("获取天气信息失败：%s", str(e))
            return {"error": str(e)}
        except Exception as e:
            logger.exception("未知错误")
            return {"error": f"未知错误：{str(e)}"}


if __name__ == '__main__':
    cities = ["固原"]
    for city in cities:
        result = QWeatherService.get_weather_info(city, 2, 7)
        print(f"{city}的天气信息：{result}")
        # 测试获取预警信息
        alert_result = QWeatherService.get_weather_info(city, 4)
        print(f"{city}的天气预警信息：{alert_result}")
        # 测试获取天气特征信息
        current = QWeatherService.get_weather_info(city, 1, 7)
        print(f"{city}当前的天气特征信息：{current}")

