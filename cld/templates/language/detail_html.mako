<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

<div class="alert alert-warning">
    <em>Languages</em> in this catalog are defined as
    <a href="https://glottolog.org/glottolog/glottologinformation">spoken L1 languages in Glottolog</a>.
</div>

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="reference"><a href="#reference" data-toggle="tab">References</a></li>
        <li class="active datapoint"><a href="#datapoint" data-toggle="tab">Data Points</a></li>
        <li class="resource"><a href="#resource" data-toggle="tab">Resources</a></li>
        <li class="source"><a href="#source" data-toggle="tab">Sources</a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="reference" class="tab-pane reference">
            ${request.get_datatable('valuesets', h.models.ValueSet, language=ctx).render()}
        </div>
        <div id="datapoint" class="tab-pane active datapoint">
            ${request.get_datatable('values', h.models.Value, language=ctx).render()}
        </div>
        <div id="resource" class="tab-pane resource">
            ${request.get_datatable('contributions', h.models.Contribution, language=ctx).render()}
        </div>
        <div id="source" class="tab-pane source">
            ${request.get_datatable('sources', h.models.Source, language=ctx).render()}
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



<%def name="sidebar()">
    <div class="well well-small">
        ${request.map.render()}
        ${h.format_coordinates(ctx)}

        <dl>
            <dt>Glottocode:</dt>
            <dd>${ctx.glottocode}</dd>
        <dt>Macroarea:</dt>
        <dd>${h.link(req, ctx.macroarea_obj)}</dd>
        </dl>
    </div>
</%def>
