from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

import main.models as models
import api.shop.serializer as serializers


class ShopCategoryView(ListModelMixin, GenericViewSet):
	queryset = models.ShopCategory.objects.only("name")
	serializer_class = serializers.ShopCategorySerializer


class ShopView(ListModelMixin, GenericViewSet):
	queryset = models.Shop.objects.select_related("category")
	serializer_class = serializers.ShopSerializer

	def get_queryset(self):
		qs = self.queryset
		category = self.request.query_params.get("category", None)
		if category:
			qs = qs.filter(category_id=category)
		return qs

