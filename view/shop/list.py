from django.views import View
from django.shortcuts import render


class ShopListView(View):
	template_name = 'pages/shop/list.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

