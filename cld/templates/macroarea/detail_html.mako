<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "macroareas" %>
<%block name="title">${_('Macroarea')} ${ctx.name}</%block>

<h2>${_('Macroarea')} ${ctx.name}</h2>

<p>${ctx.description}</p>

${lmap.render()}

${request.get_datatable('languages', h.models.Language, macroarea_obj=ctx).render()}
