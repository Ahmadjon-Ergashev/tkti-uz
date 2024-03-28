from rest_framework import serializers

import main.models as models


class ShopCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = models.ShopCategory
		fields = ("id", "name")


class ShopSerializer(serializers.ModelSerializer):
	category = ShopCategorySerializer()

	class Meta:
		model = models.Shop
		fields = (
			"id", "category", "name", "image",
			"price", "contact", "phone_number", "telegram", "instagram"
		)
		