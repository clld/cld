from clld.web.maps import Map, Layer
from clld.db.meta import DBSession
from clld.web.util.helpers import link

from clld.web.maps import GeoJsonSelectedLanguages, SelectedLanguagesMap

from cld.models import Macroarea


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
    pass
