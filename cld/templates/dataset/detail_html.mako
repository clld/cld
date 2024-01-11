<%inherit file="../home_comp.mako"/>

<h2>Catalog of Linguistic Diversity</h2>

<div class="alert alert-info">
    This is a mockup of the Catalog of Linguistic Diversity. It only serves for illustrating the
    scope and functionality this catalog could have.
</div>

<p>
    Browsing the catalog by <a href="${req.route_url('macroareas')}">macroarea</a> provides an overview
    on the spoken L1 languages of a linguistic macroarea, tagged for documentation status in terms of
    the Boasian triad - based on information from Glottolog's bibliography.
</p>

<p>
    This mockup also provides two examples listing linguistic data resources beyond what is described
    in Glottolog:
</p>
<ul>
    <li><a href="${req.route_url('language', id='mans1258')}">Northern Mansi</a> - a small uralic language from Northern Eurasia</li>
    <li><a href="${req.route_url('language', id='stan1295')}">Standard German</a> - a national language of a Western European country</li>
</ul>
