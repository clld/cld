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


@implementer(interfaces.ILanguage)
class Variety(CustomModelMixin, common.Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    glottocode = Column(Unicode)
    macroarea_obj_pk = Column(Integer, ForeignKey('macroarea.pk'))
    macroarea_obj = relationship(Macroarea, backref='languages')

    has_grammar = Column(Boolean, default=False)
    has_dictionary = Column(Boolean, default=False)
    has_text = Column(Boolean, default=False)


@implementer(interfaces.IParameter)
class Feature(CustomModelMixin, common.Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
