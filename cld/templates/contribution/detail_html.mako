<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<h2>${_('Contribution')} ${ctx.name}</h2>

<div class="alert alert-info">
    Resources are instances of sources from which references are extracted.
</div>


<h3>References</h3>

<% dt = request.get_datatable('valuesets', h.models.ValueSet, contribution=ctx) %>
% if dt:
<div>
    ${dt.render()}
</div>
% endif
