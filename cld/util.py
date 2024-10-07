from clld.web.maps import SelectedLanguagesMap

from cld import models
from cld.maps import MacroareaMap
from cld.maps import MacroareaLanguagesGeoJson


def macroarea_index_html(request=None, context=None, **kw):
    return {
        'macroareamap': MacroareaMap(context, request),
    }


def macroarea_detail_html(request=None, context=None, **kw):
    return {
        'lmap': SelectedLanguagesMap(
            context, request, context.languages, geojson_impl=MacroareaLanguagesGeoJson)
    }
