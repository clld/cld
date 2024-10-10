import pathlib
import itertools
import collections

from sqlalchemy.orm import joinedload
from clldutils.misc import nfilter
from clldutils.color import qualitative_colors
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from clld_glottologfamily_plugin.util import load_families
from pyglottolog import Glottolog
from csvw.dsv import reader

from pycldf import Sources


import cld
from cld import models


def main(args):
    data = Data()
    data.add(
        common.Dataset,
        cld.__name__,
        id=cld.__name__,
        domain='cld.clld.org',

        publisher_name = "",
        publisher_place = "",
        publisher_url = "",
        license = "http://creativecommons.org/licenses/by/4.0/",
        jsondata = {
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'},

    )
    d = pathlib.Path(__file__).parent
    gl = Glottolog(args.glottolog)

    for ma in gl.macroareas.values():
        data.add(
            models.Macroarea, ma.name,
            id=ma.id, name=ma.name, description=ma.description, jsondata=ma.geojson)

    for lang in [
        dict(id='mans1258', name='Northern Mansi', latitude=64.41, longitude=61.34, Macroarea='Eurasia'),
        dict(id='phom1236', name='Phom Naga', latitude=26.4715, longitude=94.7476, Macroarea='Eurasia'),
    ]:
        data.add(
            models.Variety,
            lang['id'],
            id=lang['id'],
            name=lang['name'],
            latitude=lang['latitude'],
            longitude=lang['longitude'],
            glottocode=lang['id'],
            macroarea_obj=data['Macroarea'][lang['Macroarea']],
        )

    for rec in bibtex.Database.from_file(d / 'mansi.bib', lowercase=True):
        s = data.add(common.Source, rec.id, _obj=bibtex2source(rec))
        DBSession.flush()
        DBSession.add(common.LanguageSource(language_pk=data['Variety']['mans1258'].pk, source_pk=s.pk))

    for rec in bibtex.Database.from_file(d / 'phom.bib', lowercase=True):
        s = data.add(common.Source, rec.id, _obj=bibtex2source(rec))
        DBSession.flush()
        DBSession.add(common.LanguageSource(language_pk=data['Variety']['phom1236'].pk, source_pk=s.pk))

    for param in reader(d / 'bit.csv', dicts=True):
        data.add(
            models.Bit,
            param['ID'],
            id=param['ID'],
            knowledgedomain=param['Domain'],
            name=param['Parameter'] if param['Parameter'] != 'Structural Data' else 'Structural Data ({})'.format(param['Domain']),
            description=param['Note'],
        )

    for id_, name, src in [
        ('riese2001', 'Riese 2001: Vogul', '103074'),
        ('romb1982', "Rombandeeva, Evdokija and E. A. Kuzakova 1982: Slovar' Mansijsko-Russkij i Russko-Mansijskij", '550166'),
        ('honkola2013', 'Honkola et al. 2013', 'Honkola2013'),
        ('bano2008', 'Bano 2008: A descriptive study of Phom language', '139594'),
    ]:
        data.add(models.Resource, id_, id=id_, name=name, description='', source=data['Source'][src])

    for id_, lid, rid, bit in [
        ('riese2001_11_17', 'mans1258', 'riese2001', '01'),
        ('romb1982', 'mans1258', 'romb1982', '11'),
        ('honkola2013', 'mans1258', 'honkola2013', '47'),
        ('bano2008_120_185_a', 'phom1236', 'bano2008', '01'),
        ('bano2008_120_185_b', 'phom1236', 'bano2008', '02'),
        ('bano2008_186_259', 'phom1236', 'bano2008', '08'),
    ]:
        data.add(models.Reference, id_, id=id_, language=data['Variety'][lid], contribution=data['Resource'][rid], parameter=data['Bit'][bit])

    for id_, name, desc in [
        ('phonotacticon', 'Phonotacticon', 'Joo, I., & Hsu, Y.-Y. (2024). Phonotacticon (1.0).'),
        ('dplace', 'D-PLACE', 'Kirby et al. (2016): D-Place'),
        ('northeuralex', 'NorthEuralex', 'Dellert, J. et al. (2020): NorthEuralex.'),
        ('phoible', 'Phonetics Information Base and Lexicon', 'Moran, S. and McCloy, D.  (2019): PHOIBLE.'),
        ('europhon', 'The Database of Eurasian Phonological Inventories', 'Nikolaev, D. (2018): Database of Eurasian Phonological Inventories.'),
    ]:
        data.add(models.Database, id_, id=id_, name=name, description=desc)

    for i, (refid, sid, dbid, url, bitid) in enumerate([
        ('bano2008_120_185_b',
         '139594',
         'phonotacticon',
         'https://doi.org/10.5281/zenodo.10623743',
         '02'),
        ('riese2001_11_17',
         '103074',
         'phoible',
         'https://phoible.org/inventories/view/2475#tipa',
         '01'),
        ('riese2001_11_17',
         '103074',
         'europhon',
         'https://eurphon.info/languages/html?lang_id=86',
         '01'),
        ('romb1982',
         '550166',
         'northeuralex',
         'http://northeuralex.org/languages/mns',
         '16'),
        ('honkola2013',
         'Honkola2013',
         'dplace',
         'https://d-place.org/phylogenys/honkola_et_al2013',
         '47'),
    ]):
        obj = data.add(
            models.Datapoint,
            str(i + 1),
            id=str(i + 1),
            valueset=data['Reference'][refid],
            source=data['Source'][sid],
            database=data['Database'][dbid],
            bit=data['Bit'][bitid],
            location=url
        )
        obj.name = '{} {} for {} based on {}'.format(
            obj.database.name,
            obj.valueset.parameter.name,
            obj.valueset.language.name,
            obj.source.name)

    load_families(
        Data(),
        [(l.glottocode, l) for l in data['Variety'].values()],
        glottolog_repos=args.glottolog,
        isolates_icon='tcccccc',
        strict=False,
    )


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for bit in DBSession.query(models.Bit).options(joinedload(common.Parameter.valuesets)):
        bit.lcount = len(set(vs.language_pk for vs in bit.valuesets))

    for bit in DBSession.query(models.Bit).options(joinedload(models.Bit.datapoints)):
        bit.ldpcount = len(set(dp.valueset.language_pk for dp in bit.datapoints))

    for lang in DBSession.query(models.Variety).options(joinedload(common.Language.valuesets)):
        lang.bitcount = len(set(vs.parameter_pk for vs in lang.valuesets))

    for db in DBSession.query(models.Database).options(joinedload(models.Database.datapoints)):
        db.domains = ' / '.join(sorted(set(dp.valueset.parameter.knowledgedomain for dp in db.datapoints)))
        db.dpcount = len(db.datapoints)
