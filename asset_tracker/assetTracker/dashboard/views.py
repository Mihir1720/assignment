# Chart file.
from assets.models import Assets
from assets.serializers import AssetSerializer
from django.shortcuts import render
from rest_framework.views import APIView


class PieChartHandler(APIView):
    """
    PieChart API
    Allowed Methods: 
        GET
    Args:
        Request object
    Django Context(will be used in html template):
        {"labels": [<asset types>], "data": [<asset types' count>]}
        {"labels": ["Laptop", "Mobile"], "data": [1, 1]}
    Returns:
        Render a HTML template.
    """

    def get(self, request):
        data = {}

        assets = Assets.get_all()
        serializer = AssetSerializer(assets, many=True)
        for asset in serializer.data:
            type = asset.get("asset_type")
            if type in data:
                data[type] += 1
            else:
                data[type] = 1
    
        return render(
            request, 
            "dashboard/pie_chart.html", 
            {
                "labels": list(data.keys()), 
                "data": list(data.values())
            }
        )

class BarChartHandler(APIView):
    """
    BarChart API
    Allowed Methods: 
        GET
    Args:
        Request object
    Django Context(will be used in html template):
        {"activeAssets": [<active assets' count>], "inactiveAssets": [inactive assets' count>]}
        {"activeAssets": [2, 2], "inactiveAssets": [1, 1]}
    Returns:
        Render a HTML template.
    """

    def get(self, request):
        data = {"active": 0, "inActive": 0}

        assets = Assets.get_all()
        serializer = AssetSerializer(assets, many=True)
        for asset in serializer.data:
            if asset.get("is_active", "No") == "Yes":
                data["active"] += 1
            else:
                data["inActive"] += 1

        return render(
            request, 
            "dashboard/bar_chart.html", 
            {
                "labels": ["Active", "Inactive"], 
                "data": [data.get("active", 0), data.get("inActive", 0)]
            }
        )
