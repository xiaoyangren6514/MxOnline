from django.shortcuts import render
from django.views.generic import View

from .models import CityDict, CourseOrg


# Create your views here.
class OrgView(View):
    def get(self, request):
        all_cities = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()
        orgs_count = all_orgs.count()
        return render(request, 'org-list.html', {
            'all_cities': all_cities,
            'all_orgs': all_orgs,
            'orgs_count': orgs_count
        })
