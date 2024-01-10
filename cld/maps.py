import collections

from clld.web.maps import Map, Layer
from clld.db.meta import DBSession
from clld.web.util.helpers import link
from clldutils.svg import pie, data_url

from clld.web.maps import GeoJsonSelectedLanguages, SelectedLanguagesMap

from cld.models import Macroarea

COLORS = collections.OrderedDict(
    zip(['grammar', 'dictionary', 'text'], ['#4477AA', '#DDCC77', '#CC6677']))


def feature(req, ma):
    return dict(
        type='Feature',
        properties=dict(
            label=ma.name,
            description='<h3>{}</h3>'.format(link(req, ma)) + '<p>' + ma.description + '</p>'),
        geometry=ma.jsondata['features'][0]['geometry'])


class MacroareaMap(Map):
    def get_layers(self):
        yield Layer(
            'macroareas',
            'macroareas',
             {
        'type': 'FeatureCollection',
        'properties': {'layer': 'macroareas'},
        'features': [feature(self.req, ma) for ma in DBSession.query(Macroarea)]},
            addToLayersControl=True,
        )


class MacroareaLanguagesGeoJson(GeoJsonSelectedLanguages):
    def feature_properties(self, ctx, req, feature):
        """paint icon"""
        return {
            'icon': data_url(pie(
                [1, 1, 1],
                [color if getattr(feature, 'has_' + attr) else '#ffffff' for attr, color in COLORS.items()])),
            'language': feature}
