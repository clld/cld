from sqlalchemy.orm import joinedload
from clld.db.util import get_distinct_values
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web.datatables.language import Languages
from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.datatables import FamilyCol

from cld import models


class CldLanguages(Languages):
    def base_query(self, query):
        return query.outerjoin(Family).options(joinedload(models.Variety.family)).distinct()

    def col_defs(self):
        return [
            LinkCol(self, 'id'),
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
