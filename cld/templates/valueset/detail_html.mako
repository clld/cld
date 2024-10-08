<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<h2>Reference ${h.link(request, ctx.language)}/${h.link(request, ctx.parameter)}</h2>

<div class="alert alert-warning">
    <p>References describe instances of <a href="${req.route_url('parameters')}">basic information types</a>
        for particular languages found in resources. If the information is available
        in structured form in a database, this will be recorded as data point associated with the
        reference.</p>
    <p>References without associated data points signal the potential (or the need) for further
    standardisation by extracting the information into structured data.</p>
</div>

% if ctx.values:
<h3> Data points</h3>
<ul>
% for v in ctx.values:
    <li>${h.link(req, v)}</li>
% endfor
</ul>
% endif

<%def name="sidebar()">
<div class="well well-small">
<dl class="dl-horizontal">
    <dt class="contribution">${_('Contribution')}:</dt>
    <dd class="contribution">
        ${h.link(request, ctx.contribution)}
        by
        ${h.linked_contributors(request, ctx.contribution)}
        ${h.button('cite', onclick=h.JSModal.show(ctx.contribution.name, request.resource_url(ctx.contribution, ext='md.html')))}
    </dd>
    <dt class="language">${_('Language')}:</dt>
    <dd class="language">${h.link(request, ctx.language)}</dd>
    <dt class="parameter">${_('Parameter')}:</dt>
    <dd class="parameter">${h.link(request, ctx.parameter)}</dd>
    % if ctx.references or ctx.source:
    <dt class="source">${_('Source')}:</dt>
        % if ctx.source:
        <dd>${ctx.source}</dd>
        % endif
        % if ctx.references:
        <dd class="source">${h.linked_references(request, ctx)|n}</dd>
        % endif
    % endif
    ${util.data(ctx, with_dl=False)}
</dl>
</div>
</%def>
