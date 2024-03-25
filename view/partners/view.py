from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

import main.models as models


class PartnersView(View):
	template_name = 'pages/partners/partners.html'

	def get(self, request):
		country = models.Country.objects.only("name")
		return render(request, self.template_name, {
			"country": country,
			"title": _("Hamkor universitet va tashkilotlar")
		})
