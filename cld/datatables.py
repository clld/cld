from sqlalchemy.orm import joinedload
from clld.db.util import get_distinct_values
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol, DataTable, IdCol
from clld.web.datatables.language import Languages
from clld.web.datatables.value import Values, ValueNameCol
from clld.web.datatables.valueset import Valuesets
from clld.web.datatables.contribution import Contributions
from clld.web.datatables.source import Sources
from clld.web.datatables.parameter import Parameters
from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.datatables import FamilyCol

from clld.db.models import common

from cld import models


class Macroareas(DataTable):
    def col_defs(self):
        return [
            IdCol(self, 'id'),
            LinkCol(self, 'name'),
        ]


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
                FamilyCol(self, 'Family', models.Variety),
                LinkToMapCol(self, '#'),
            ]
        return [
            IdCol(self, 'id'),
            Col(self, 'name'),
            Col(self, 'bits', sTitle='#BIT', model_col=models.Variety.bitcount),
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


class References(Valuesets):
    def col_defs(self):
        if self.parameter:
            return [
                LinkCol(self,
                        'language',
                        sTitle=self.req.translate('Language'),
                        model_col=common.Language.name,
                        get_object=lambda i: i.language),
                LinkCol(self,
                        'contribution',
                        sTitle=self.req.translate('Contribution'),
                        model_col=common.Contribution.name,
                        get_object=lambda i: i.contribution),
            ]
        if self.contribution:
            return [
                LinkCol(self, 'id'),
                LinkCol(self,
                        'language',
                        sTitle=self.req.translate('Language'),
                        model_col=common.Language.name,
                        get_object=lambda i: i.language),
                LinkCol(self,
                        'parameter',
                        sTitle=self.req.translate('Parameter'),
                        model_col=common.Parameter.name,
                        get_object=lambda i: i.parameter),
            ]

        return [
            LinkCol(self, 'id'),
            Col(self,
                'domain',
                choices=get_distinct_values(models.Bit.knowledgedomain),
                get_object=lambda i: i.parameter,
                model_col=models.Bit.knowledgedomain,
                ),
            LinkCol(self,
                    'parameter',
                    sTitle=self.req.translate('Parameter'),
                    model_col=common.Parameter.name,
                    get_object=lambda i: i.parameter),
            LinkCol(self,
                    'contribution',
                    sTitle=self.req.translate('Contribution'),
                    model_col=common.Contribution.name,
                    get_object=lambda i: i.contribution),
        ]


class Datapoints(Values):
    __constraints__ = Values.__constraints__ + [models.Database]

    def base_query(self, query):
        query = query.join(common.ValueSet).options(
            joinedload(common.Value.valueset)
        )

        if self.language:
            query = query.join(models.Datapoint.bit)
            return query.filter(common.ValueSet.language_pk == self.language.pk)

        if self.parameter:
            query = query.join(common.ValueSet.language).join(models.Datapoint.bit)
            return query.filter(models.Datapoint.bit_pk == self.parameter.pk)

        if self.contribution:
            query = query.join(models.Datapoint.bit)
            return query.filter(common.ValueSet.contribution_pk == self.contribution.pk)

        if self.database:
            return query\
                .join(models.Datapoint.bit)\
                .join(models.Datapoint.database).filter(models.Database.pk == self.database.pk)
        return query

    def col_defs(self):
        if self.parameter:
            return [
                LinkCol(
                    self,
                    'language',
                    sTitle=self.req.translate('Language'),
                    model_col=common.Language.name,
                    get_object=lambda i: i.valueset.language),
                LinkCol(
                    self,
                    'datapoint',
                ),
                LinkCol(
                    self,
                    'database',
                    get_object=lambda i: i.database,
                )
            ]
        res = [
            Col(self,
                'domain',
                choices=get_distinct_values(models.Bit.knowledgedomain),
                get_object=lambda i: i.bit,
                model_col=models.Bit.knowledgedomain,
            ),
            LinkCol(
                self,
                'parameter',
                sTitle=self.req.translate('Parameter'),
                model_col=common.Parameter.name,
                get_object=lambda i: i.bit),
            LinkCol(
                self, 'value', get_object=lambda i: i),
        ]
        if self.database:
            res.extend([
                LinkCol(
                    self,
                    'language',
                    sTitle=self.req.translate('Language'),
                    model_col=common.Language.name,
                    get_object=lambda i: i.valueset.language),
            ])
        return res


class Bits(Parameters):
    def col_defs(self):
        return [
            Col(self,
                'domain',
                choices=get_distinct_values(models.Bit.knowledgedomain),
                model_col=models.Bit.knowledgedomain,
            ),
            LinkCol(
                self,
                'parameter',
                sTitle=self.req.translate('Parameter'),
            ),
            Col(self, 'langs', sTitle='#Languages with reference', model_col=models.Bit.lcount),
            Col(self, 'langs', sTitle='#Languages with datapoint', model_col=models.Bit.ldpcount),
            Col(self, 'description'),
        ]

    def get_options(self):
        opts = super(Parameters, self).get_options()
        opts['aaSorting'] = [[2, 'desc'], [0, 'asc']]
        return opts


class Resources(Contributions):
    __constraints__ = [common.Language]

    def base_query(self, query):
        if self.language:
            query = query.join(common.ValueSet).join(common.Language).filter(common.Language.pk == self.language.pk)
        return query


class CLDSources(Sources):
    __constraints__ = [common.Language]

    def base_query(self, query):
        if self.language:
            query = query.join(common.LanguageSource).join(common.Language).filter(common.Language.pk == self.language.pk)
        return query


class Databases(DataTable):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'dpcount', sTitle='#Data points'),
            Col(self, 'domains'),
        ]


def includeme(config):
    """register custom datatables"""
    config.register_datatable('sources', CLDSources)
    config.register_datatable('contributions', Resources)
    config.register_datatable('parameters', Bits)
    config.register_datatable('values', Datapoints)
    config.register_datatable('valuesets', References)
    config.register_datatable('languages', CldLanguages)
    config.register_datatable('macroareas', Macroareas)
    config.register_datatable('databases', Databases)
