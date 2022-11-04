from django.conf import settings


def site_id(request):
    return {"siteID": settings.SITE_ID}
