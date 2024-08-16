import collections

from pyramid.config import Configurator
from clld.interfaces import IMapMarker, IValueSet, IValue, IDomainElement
from clld.web.icon import MapMarker
from clldutils.svg import pie, icon, data_url
from clld_glottologfamily_plugin import util
from clld.web import app

# we must make sure custom models are known at database initialization!
from cld import models
from cld import interfaces
from cld import views


class LanguageByFamilyMapMarker(util.LanguageByFamilyMapMarker):
    def __call__(self, ctx, req):
        try:
            if IValueSet.providedBy(ctx):
                c = collections.Counter([v.domainelement.jsondata['color'] for v in ctx.values])
                return data_url(pie(*list(zip(*[(v, k) for k, v in c.most_common()])), **dict(stroke_circle=True)))
            if IDomainElement.providedBy(ctx):
                return data_url(icon(ctx.jsondata['color'].replace('#', 'c')))
            if IValue.providedBy(ctx):
                return data_url(icon(ctx.domainelement.jsondata['color'].replace('#', 'c')))
        except AttributeError:
            pass
        return super(LanguageByFamilyMapMarker, self).__call__(ctx, req)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')
    config.register_resource('macroarea', models.Macroarea, interfaces.IMacroarea, with_index=True)

    config.registry.registerUtility(LanguageByFamilyMapMarker(), IMapMarker)

    return config.make_wsgi_app()
