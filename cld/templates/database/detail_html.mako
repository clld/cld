<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "databases" %>
<%block name="title">${_('Database')} ${ctx.name}</%block>

<h2>${_('Database')} ${ctx.name}</h2>

<p>${ctx.description}</p>


${request.get_datatable('values', h.models.Value, database=ctx).render()}
