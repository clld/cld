<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>




<h2>${_('Parameter')} ${ctx.name}</h2>

<div class="alert alert-warning">
    <a href="${req.route_url('parameters')}">Basic information types</a> are well understood types
    of linguistic data which are useful for comparative study of languages.
</div>

% if ctx.description:
<div class="well">
<p>${ctx.description}</p>
</div>
% endif

<div style="clear: both"/>

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active reference"><a href="#reference" data-toggle="tab">References</a></li>
        <li class="datapoint"><a href="#datapoint" data-toggle="tab">Data Points</a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="reference" class="tab-pane active reference">
            ${request.get_datatable('valuesets', h.models.ValueSet, parameter=ctx).render()}
        </div>
        <div id="datapoint" class="tab-pane datapoint">
            ${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
        </div>
    </div>
    <script>
        $(document).ready(function() {
            if (location.hash !== '') {
                $('a[href="#' + location.hash.substr(2) + '"]').tab('show');
            }
            return $('a[data-toggle="tab"]').on('shown', function(e) {
                return location.hash = 't' + $(e.target).attr('href').substr(1);
            });
        });
    </script>
</div>

