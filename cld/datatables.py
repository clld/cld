from sqlalchemy.orm import joinedload
from clld.db.util import get_distinct_values
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol, DataTable, IdCol
from clld.web.datatables.language import Languages
from clld.web.datatables.value import Values
from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.datatables import FamilyCol

from cld import models


class Macroareas(DataTable):
    def col_defs(self):
        return [
            IdCol(self, 'id'),
            LinkCol(self, 'name'),
        ]


class HasBoasItemCol(Col):
    def __init__(self, dt, name, **kw):
        kw['sClass'] = name
        kw['model_col'] = getattr(models.Variety, 'has_' + name)
        Col.__init__(self, dt, name, **kw)
        self._attr = name

    def format(self, item):
        return '✓' if getattr(item, 'has_' + self._attr) else ''


class CldLanguages(Languages):
    __constraints__ = [models.Macroarea]

    def base_query(self, query):
        res = query.outerjoin(Family).options(joinedload(models.Variety.family)).distinct()
        if self.macroarea_obj:
            res = res.filter(models.Variety.macroarea_obj_pk == self.macroarea_obj.pk)

        return res

    @staticmethod
    def attr_from_constraint(model):
        return 'macroarea_obj'

    def col_defs(self):
        if self.macroarea_obj:
            return [
                IdCol(self, 'id'),
                LinkCol(self, 'name'),
                HasBoasItemCol(self, 'grammar'),
                HasBoasItemCol(self, 'dictionary'),
                HasBoasItemCol(self, 'text'),
                FamilyCol(self, 'Family', models.Variety),
                LinkToMapCol(self, '#'),
            ]
        return [
            IdCol(self, 'id'),
            Col(self, 'name'),
            FamilyCol(self, 'Family', models.Variety),
            Col(self, 'latitude'),
            Col(self, 'longitude'),
            LinkToMapCol(self, '#'),
            Col(self, 'macroarea',
                model_col=models.Variety.macroarea,
                choices=get_distinct_values(models.Variety.macroarea)),
            #
            #
            #
        ]


def includeme(config):
    """register custom datatables"""
    config.register_datatable('languages', CldLanguages)
    config.register_datatable('macroareas', Macroareas)
