from rest_framework import serializers
from assets.models import AssetTypes, Assets
from common import utils
from assets.models import AssetImages

class AssetTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetTypes
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["created_at"] = utils.convert_datetime_to_string(datetime_obj=representation.get("created_at"))
        representation["updated_at"] = utils.convert_datetime_to_string(datetime_obj=representation.get("updated_at"))
        
        return representation
    
class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assets
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["is_active"] = "Yes" if instance.is_active else "No"
        asset_type = AssetTypes.get_by_id(id=instance.asset_type.id)
        representation["asset_type"] = asset_type.type
        asset_images = AssetImages.get_by_asset_id(asset_id=instance.id)
        representation["asset_images"] = asset_images if asset_images else None
        representation["created_at"] = utils.convert_datetime_to_string(datetime_obj=representation.get("created_at"))
        representation["updated_at"] = utils.convert_datetime_to_string(datetime_obj=representation.get("updated_at"))
        
        return representation