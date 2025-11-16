from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from myapi.utils.Qweatherinfo import QWeatherService


# Create your views here.

class MeteorologyViewSet(ViewSet):
    def list(self, request):
        addresses = request.data.get("address") or request.query_params.get("address")
        choose = request.data.get("choose") or request.query_params.get("choose")
        days = request.data.get("days") or request.query_params.get("days")
        if not choose:
            choose = 3
        else:
            choose = int(choose)
        if not days:
            days = 3
        else:
            days = int(days)
        if not addresses:
            addresses = "银川"
        else:
            addresses = addresses.split(",")
        results = []
        for addr in addresses:
            if "市" in addr:
                addr = addr.replace("市", "")
            try:
                weather_info = QWeatherService.get_weather_info(addr, choose, days)
                if weather_info is None:
                    continue
                results.append(weather_info)
            except Exception as e:
                results.append({addr: str(e)})
        return Response(results, status=status.HTTP_200_OK)
