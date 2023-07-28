from rest_framework.views import APIView
from assets.models import AssetTypes, Assets, AssetImages
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from common import messages, utils
from assetTracker.settings import PAGINATION
from django.http import HttpResponse
import csv
from django.db import transaction

class AssetTypesHandler(APIView):
    """
    AssetTypes API
    Allowed Methods: 
        GET
        POST
        PUT
        DELETE
    Args:
        Request object
    Returns:
        sample response:
            {"success": True/False, "message": "<some message>", "data": <list_of_dict>}
    """

    def get(self, request):
        """
        List all asset types.
        Args:
            page: Optional(Default: 1)
        Returns:
            [
                {
                    "success": True,
                    "message": "<in case of success false>", 
                    "data": [
                        {
                            "id": 1, 
                            "type": "Laptop", 
                            "description": "This is laptop.", 
                            "createdAt": "27-07-2023 15:03", 
                            "updatedAt": "27-07-2023 15:03"
                        }
                    ]
                }
            ]
,       """
        asset_types = AssetTypes.get_all()
        if asset_types:
            response_data = []
            paginator = Paginator(asset_types, PAGINATION)
            page_number = request.GET.get("page")
            if page_number:
                try:
                    asset_types = paginator.page(page_number).object_list
                except Exception:
                    # Invalid Page Number.
                    return Response({"success": False, "message": messages.get_message("INVALID_PAGE_NUMBER")}, status=status.HTTP_200_OK)
            for asset_type in asset_types:
                response_data.append(
                    {
                        "id": str(asset_type.id),
                        "type": asset_type.type, 
                        "description": asset_type.description, 
                        "createdAt": utils.convert_datetime_to_string(datetime_obj=asset_type.created_at),
                        "updatedAt": utils.convert_datetime_to_string(datetime_obj=asset_type.updated_at), 
                    }
                )
            return Response({"success": True, "data": response_data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": True, "message": messages.get_message("NO_ASSET_TYPES_FOUND")}, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Add an asset type.
        Args:
            type: Required
            description: Optional
        Returns:
            {
                "success": True,
                "message": ""
            }
        """
        data = request.data
        if not data.get("type"):
            return Response({"success": False, "message": messages.get_message("ASSET_TYPE_IS_MISSING")}, status=status.HTTP_200_OK)
        asset_type_obj = AssetTypes.add(type=data.get("type"), description=data.get("description", ""))
        if asset_type_obj:
            return Response({"success": True, "message": messages.get_message("ASSET_TYPE_ADD_SUCCESSFUL")}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": messages.get_message("SOMETHING_WENT_WRONG")}, status=status.HTTP_200_OK)
    
    def put(self, request):
        """
        Update an asset type.
        Args:
            id: asset type id - Required
            type: Optional
            description: Optional
        Returns:
            {
                "success": True,
                "message": ""
            }
        """
        data = request.data
        if data.get("id") is None:
            return Response({"success": False,"message": messages.get_message("INVALID_ASSET_TYPE")}, status=status.HTTP_200_OK)
        else:
            updated_values = {}
            if data.get("type"):
                asset_type_obj = AssetTypes.get_by_type(type=data.get("type"))
                if asset_type_obj:
                    return Response({"success": False,"message": messages.get_message("ASSET_TYPE_ALREADY_EXIST")}, status=status.HTTP_200_OK)
                updated_values.update({"type": data.get("type")})
            if data.get("description"):
                updated_values.update({"description": data.get("description")})
            asset_type_obj = AssetTypes.update(id=data.get("id"), updated_values=updated_values)
            if asset_type_obj:
                return Response({"success": True, "message": messages.get_message("ASSET_TYPE_UPDATE_SUCCESSFUL")}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": messages.get_message("SOMETHING_WENT_WRONG")}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        """
        Delete an asset type.
        Args:
            id: asset type id
        Returns:
            {
                "success": True,
                "message": ""
            }
        """
        data = request.GET
        if data.get("id") is None:
            return Response({"success": False, "message": messages.get_message("INVALID_ASSET_TYPE")}, status=status.HTTP_200_OK)
        else:
            AssetTypes.delete_by_id(id=data.get("id"))
            return Response({"success": True, "message": messages.get_message("ASSET_TYPE_DELETE_SUCCESSFUL")}, status=status.HTTP_200_OK)

class AssetsHandler(APIView):
    """
    Assets API
    Allowed Methods: 
        GET
        POST
        PUT
        DELETE
    Args:
        Request object
    Returns:
        sample response:
            {"success": True/False, "message": "<some message>", "data": <list_of_dict>}
    """

    def get_asset_data(self, asset, for_report=False):
        asset_data = {}
        asset_type = AssetTypes.get_by_id(id=asset.asset_type.id)
        if asset_type:
            asset_type = asset_type.type
            asset_images = list(set(AssetImages.get_by_asset_id(asset_id=asset.id)))
            asset_data = {
                    "name": asset.name, 
                    "isActive": asset.is_active,
                    "assetType": asset_type, 
                    "assetImages": asset_images,
                    "createdAt": utils.convert_datetime_to_string(datetime_obj=asset.created_at),
                    "updatedAt": utils.convert_datetime_to_string(datetime_obj=asset.updated_at) 
                }
            if for_report is False:
                asset_data.update({"id": str(asset.id)})   
        return asset_data

    def get(self, request):
        """
        List all asset types.
        Args:
            None
        Returns:
            [
                {
                    "success": True,
                    "message": "<in case of success false>", 
                    "data": [
                        {
                            "id": 1, 
                            "name": "Macbook", 
                            "isActive": True, 
                            "assetType": "Laptop",
                            "assetImages": [],
                            "createdAt": "27-07-2023 15:03", 
                            "updatedAt": "27-07-2023 15:03"
                        }
                    ]
                }
            ]
,       """
        assets = Assets.get_all()
        if assets:
            response_data = []
            for asset in assets:
                asset_data = self.get_asset_data(asset=asset)
                if asset_data:
                    response_data.append(asset_data)
            return Response({"success": True, "data": response_data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": True, "message": messages.get_message("NO_ASSETS_FOUND")}, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Add an asset.
        Args:
            name: Required
            assetTypeId: Required
            assetImages: Optional
        Returns:
            {
                "success": True,
                "message": ""
            }
        """
        data = request.data
        if not data.get("assetTypeId"):
            return Response({"success": False, "message": messages.get_message("CANNOT_ADD_ASSET_AS_ASSET_TYPE_IS_MISSING")}, status=status.HTTP_200_OK)
        if not data.get("name"):
            return Response({"success": False, "message": messages.get_message("ASSET_NAME_IS_MISSING")}, status=status.HTTP_200_OK)
        asset_type_obj = AssetTypes.get_by_id(id=data.get("assetTypeId"))
        if asset_type_obj:
            try:
                with transaction.atomic():
                    code = utils.get_uuid()[:16] # WE NEED TO GENERATE UUID of 16 CHARACTERS ONLY.
                    asset_obj = Assets.add(name=data.get("name"), code=code, asset_type=asset_type_obj, is_active=data.get("isActive", True))
                    if asset_obj:
                        if data.get("assetImages"):
                            asset_image_obj = AssetImages.add(asset_id=asset_obj, asset_image=data.get("assetImages"))
                            if not asset_image_obj:
                                return Response({"success": False, "message": messages.get_message("SOMETHING_WENT_WRONG")}, status=status.HTTP_200_OK)
                        return Response({"success": True, "message": messages.get_message("ASSET_ADD_SUCCESSFUL")}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"success": False, "message": messages.get_message("SOMETHING_WENT_WRONG")}, status=status.HTTP_200_OK)
            except Exception as exc:
                print("Exception occured in AssetsHandler.post as ", str(exc))
                return Response({"success": False, "message": messages.get_message("SOMETHING_WENT_WRONG")}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": messages.get_message("INVALID_ASSET_TYPE")}, status=status.HTTP_200_OK)
    
    def put(self, request):
        """
        Update an asset.
        Args:
            id: asset id - Required
            assetTypeId: Optional
            name: Optional
            isActive: Optional
        Returns:
            {
                "success": True,
                "message": ""
            }
        """
        data = request.data
        if data.get("id") is None:
            return Response({"success": False, "message": messages.get_message("INVALID_ASSET")}, status=status.HTTP_200_OK)
        else:
            updated_values = {}
            if data.get("assetTypeId"):
                asset_type_obj = AssetTypes.get_by_id(id=data.get("assetTypeId"))
                if asset_type_obj:
                    updated_values.update({"asset_type": asset_type_obj})
            if data.get("name"):
                updated_values.update({"name": data.get("name")})
            if "isActive" in data:
                updated_values.update({"is_active": data.get("isActive")})
            assets = Assets.update(id=data.get("id"), updated_values=updated_values)
            if assets:
                return Response({"success": True, "message": messages.get_message("ASSET_UPDATE_SUCCESSFUL")}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": messages.get_message("SOMETHING_WENT_WRONG")}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        """
        Delete an asset.
        Args:
            id: asset id
        Returns:
            {
                "success": True,
                "message": ""
            }
        """
        data = request.GET
        if data.get("id") is None:
            return Response({"success": False, "message": messages.get_message("INVALID_ASSET")}, status=status.HTTP_200_OK)
        else:
            Assets.delete_by_id(id=data.get("id"))
            return Response({"success": True, "message": messages.get_message("ASSET_DELETE_SUCCESSFUL")}, status=status.HTTP_200_OK)


class DownloadAssetsHandler(AssetsHandler):
    """
    Download Assets API
    Allowed Methods: 
        GET
    Args:
        Request object
    Returns:
        CSV Response.
    """

    def get(self, request):
        """
        Download all assets through CSV.
        Args:
            None
        Returns:
            CSV Response.
        """
        assets = Assets.get_all()
        if assets:
            csv_data = [["Name", "Asset Type", "Is Active", "Asset Images", "Created At", "Updated At"]]
            for asset in assets:
                asset_data = self.get_asset_data(asset=asset, for_report=True)
                if asset_data:
                    csv_data.append(
                        [
                            asset_data.get("name", ""), 
                            asset_data.get("assetType", ""), 
                            asset_data.get("isActive", ""),
                            asset_data.get("assetImages", ""),
                            asset_data.get("createdAt", ""),
                            asset_data.get("updatedAt", "")
                        ]
                    )
            
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="assets.csv"'

            writer = csv.writer(response)

            for row in csv_data:
                writer.writerow(row)

            return response