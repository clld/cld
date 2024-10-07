from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models import common
from clld_glottologfamily_plugin.models import HasFamilyMixin

import cld.interfaces

#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------

@implementer(cld.interfaces.IMacroarea)
class Macroarea(Base, common.IdNameDescriptionMixin):
    pass

# Source ffd53d

# location = local ID,
# domainofknowledge, basicinformationtype
# Value = Datapoint has dataset fk  4e78a7

# Database as custom resource!
@implementer(cld.interfaces.IDatabase)
class Database(Base, common.IdNameDescriptionMixin):
    domains = Column(Unicode)
    dpcount = Column(Integer)


# ValueSet = References  9f1e2c
@implementer(interfaces.IValueSet)
class Reference(CustomModelMixin, common.ValueSet):
    pk = Column(Integer, ForeignKey('valueset.pk'), primary_key=True)

    color = '9f1e2c'


@implementer(interfaces.IValue)
class Datapoint(CustomModelMixin, common.Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    database_pk = Column(Integer, ForeignKey('database.pk'))
    database = relationship(Database, backref='datapoints')
    source_pk = Column(Integer, ForeignKey('source.pk'))
    source = relationship(common.Source, backref='resources')
    location = Column(Unicode)


# Contribution = Resources  628d3f
@implementer(interfaces.IContribution)
class Resource(CustomModelMixin, common.Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    source_pk = Column(Integer, ForeignKey('source.pk'))
    source = relationship(common.Source, backref='cldresources')


@implementer(interfaces.ILanguage)
class Variety(CustomModelMixin, common.Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    glottocode = Column(Unicode)
    macroarea_obj_pk = Column(Integer, ForeignKey('macroarea.pk'))
    macroarea_obj = relationship(Macroarea, backref='languages')
    bitcount = Column(Integer)


@implementer(interfaces.IParameter)
class Bit(CustomModelMixin, common.Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    knowledgedomain = Column(Unicode)
    lcount = Column(Integer)
