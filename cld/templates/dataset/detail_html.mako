<%inherit file="../home_comp.mako"/>

&nbsp;
<div class="alert alert-info">
    This is a mockup of the Catalog of Linguistic Diversity. It only serves for illustrating the
    scope and functionality this catalog could have.
</div>

<p>
    This mockup also provides two examples listing linguistic data resources beyond what is described
    in Glottolog:
</p>
<ul>
    <li><a href="${req.route_url('language', id='mans1258')}">Northern Mansi</a> - a small uralic language from Northern Eurasia</li>
    <li><a href="${req.route_url('language', id='stan1295')}">Standard German</a> - a national language of a Western European country</li>
</ul>
