<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "macroareas" %>
<%block name="title">${_('Macroareas')}</%block>

<h2>${title()}</h2>
<div>
    ${macroareamap.render()}
</div>
