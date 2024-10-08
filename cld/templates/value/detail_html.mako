<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<h2>${_('Value')} ${ctx.domainelement.name if ctx.domainelement else ctx.name}</h2>

<div class="alert alert-warning">
    Data points describe extracted, structured data for a
    <a href="${req.route_url('parameters')}">basic information type</a>, corresponding to
    a reference.
</div>

</div>

<dl class="dl-horizontal">
    <dt>Language:</dt>
    <dd>${h.link(request, ctx.valueset.language)}</dd>
    <dt>${_('Parameter')}:</dt>
    <dd>${h.link(request, ctx.valueset.parameter)}</dd>
    <dt>Database:</dt>
    <dd>${h.link(request, ctx.database)}</dd>
    <dt class="source">Source:</dt>
    <dd>${h.link(request, ctx.source)}</dd>
    <dt>Location:</dt>
    <dd><a href="${ctx.location}">${ctx.location}</a></dd>
</dl>

<div class="alert alert-warning">
    Since <a href="${req.route_url('parameters')}">basic information types</a> are well understood data structures,
    the catalog may also include functionality to visualize the actual data, e.g. present
    sound inventories projected to IPA charts or interlinear glossed text with properly aligned tiers.
</div>
