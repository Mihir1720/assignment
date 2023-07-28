from django.db import models

class AssetTypes(models.Model):
    """
    Asset Types model.
    """
    class Meta:
        db_table = "asset_types"

        indexes = [
            models.Index(fields=["type"]),
        ]
    
    type = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500, default="", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_all(cls, order_by="updated_at", sort_order="DESC"):
        """
        Get all objects(asset types).
        Args:
            order_by: Optional(Default: updated_at)
            sort_order: Optional(Default: DESC)
        Returns:
            All asset types based on sorting.
        """
        if sort_order == "DESC":
            order_by = "-" + order_by
        return cls.objects.all().order_by(order_by)
    
    @classmethod
    def get_by_id(cls, id):
        """
        Get asset by id.
        Args:
            id: asset type id
        Returns:
            Asset type object.
        """
        asset_type_obj = None
        try:
            asset_type_obj = cls.objects.get(id=id)
        except Exception as exc:
            print("Exception occured in AssetTypes.get_by_id as ", str(exc))
        return asset_type_obj
    
    @classmethod
    def get_by_type(cls, type):
        """
        Get asset by type.
        Args:
            type: asset type
        Returns:
            Asset type object.
        """
        asset_type_obj = None
        try:
            asset_type_obj = cls.objects.get(type=type)
        except Exception as exc:
            print("Exception occured in AssetTypes.get_by_type as ", str(exc))
        return asset_type_obj
    
    @classmethod
    def add(cls, type, description):
        """
        Add asset type.
        Args:
            type: asset type
            description: asset type description
        Returns:
            Asset type object.
        """
        try:
            return cls.objects.create(type=type, description=description)
        except Exception as exc:
            print("Exception occured in AssetTypes.add as ", str(exc))
            return None

    @classmethod
    def update(cls, id, updated_values):
        """
        Update asset type.
        Args:
            id: asset type id
            updated_values: values to be updated({})
        Returns:
            Asset type object.
        """
        asset_type_obj = cls.get_by_id(id=id)
        for key, value in updated_values.items():
            setattr(asset_type_obj, key, value)
        asset_type_obj.save()
        return asset_type_obj
    
    @classmethod
    def delete_by_id(cls, id):
        """
        Delete asset type by id.
        Args:
            id: asset type id
        Returns:
            None.
        """
        asset_type_obj = cls.get_by_id(id=id)
        if asset_type_obj:
            asset_type_obj.delete()


class Assets(models.Model):
    """
    Assets model.
    """
    class Meta:
        db_table = "assets"
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255)
    asset_type = models.ForeignKey(AssetTypes, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_all(cls, order_by="updated_at", sort_order="DESC"):
        """
        Get all objects(assets).
        Args:
            order_by: Optional(Default: updated_at)
            sort_order: Optional(Default: DESC)
        Returns:
            All assets based on sorting.
        """
        if sort_order == "DESC":
            order_by = "-" + order_by
        return cls.objects.all().order_by(order_by)
    
    @classmethod
    def get_by_id(cls, id):
        """
        Get asset by id.
        Args:
            id: asset id
        Returns:
            Asset object.
        """
        assets_obj = None
        try:
            assets_obj = cls.objects.get(id=id)
        except Exception as exc:
            print("Exception occured in Assets.get_by_id as ", str(exc))
        return assets_obj
    
    @classmethod
    def add(cls, name, code, asset_type, is_active):
        """
        Add asset.
        Args:
            name: name of an asset
            code: 16 characters UUID(system generated)
            asset_type: AssetTypes model object
            is_active: asset is active or not(Default: True)
        Returns:
            Asset object.
        """
        return cls.objects.create(name=name, code=code, asset_type=asset_type, is_active=is_active)

    @classmethod
    def update(cls, id, updated_values):
        """
        Update asset.
        Args:
            id: asset id
            updated_values: values to be updated({})
        Returns:
            Asset object.
        """
        assets_obj = cls.get_by_id(id=id)
        for key, value in updated_values.items():
            setattr(assets_obj, key, value)
        assets_obj.save()
        return assets_obj
    
    @classmethod
    def delete_by_id(cls, id):
        """
        Delete asset by id.
        Args:
            id: asset id
        Returns:
            None.
        """
        assets_obj = cls.get_by_id(id=id)
        if assets_obj:
            assets_obj.delete()

class AssetImages(models.Model):
    """
    Asset Images model.
    """
    class Meta:
        db_table = "asset_images"

    asset_id = models.ForeignKey(Assets, on_delete=models.CASCADE)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_by_asset_id(cls, asset_id):
        """
        Get asset images by id.
        Args:
            asset_id: asset id
        Returns:
            All images matching of given asset id.
        """
        return cls.objects.filter(asset_id=asset_id).values_list("image", flat=True)

    @classmethod
    def add(cls, asset_id, asset_image):
        """
        Add asset image.
        Args:
            asset_id: Assets object.
            asset_image: asset image.
        """
        return cls.objects.create(asset_id=asset_id, image=asset_image)
    
