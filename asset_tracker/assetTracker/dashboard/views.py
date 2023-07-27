# Chart file.
from django.shortcuts import render
from assets.models import AssetTypes, Assets
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
    permission_classes = []

    def get(self, request):
        data = {}

        assets = Assets.get_all()
        for asset in assets:
            type = asset.asset_type.type
            if type in data:
                data[type] += 1
            else:
                data[type] = 1
    
        return render(request, "pie_chart.html", {"labels": list(data.keys()), "data": list(data.values())})

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

    permission_classes = []

    def get(self, request):
        data = {"active": 0, "inActive": 0}

        assets = Assets.get_all()
        for asset in assets:
            if asset.is_active is True:
                data["active"] += 1
            else:
                data["inActive"] += 1

        return render(request, "bar_chart.html", {"activeAssets": data.get("active", 0), "inactiveAssets": data.get("inActive", 0)})
