<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

% if ctx.glottocode == 'mans1258':

<ul>
<li><a href="https://uralic.clld.org/languages/26">UraTyp</a></li>
<li><a href="https://eurphon.info/languages/html?lang_id=86">EURPhon</a></li>
<li><a href="https://lexibank.clld.org/languages/northeuralex-mns">Lexibank</a></li>
<li><a href="http://northeuralex.org/languages/mns">NorthEuralex</a></li>
<li><a href="https://phoible.org/inventories/view/2475">PHOIBLE</a></li>
<li><a href="https://en.wikipedia.org/wiki/Mansi_language">Wikipedia on Mansic - the group</a></li>
<li><a href="http://www.language-archives.org/language/mns">OLAC</a></li>
<li><a href="https://archive.mpi.nl/tla/islandora/object/tla%3A1839_1A8B1F59_8FDC_4D88_9EC0_A73C3726D36C">TLA</a></li>
<li><a href="https://endangeredlanguages.com/lang/8529">ElCat</a></li>
<li><a href="https://d-place.org/society/ec15">D-PLACE</a></li>
<li><a href="https://www.elararchive.org/dk0033/">ELAR</a></li>
<li><a href="https://glottolog.org/resource/languoid/id/mans1258">Glottolog</a></li>
</ul>
    
% elif ctx.glottocode == 'stan1295':

<ul>
<li><a href="http://northeuralex.org/languages/deu">NorthEuralex</a></li>
<li><a href="https://lexibank.clld.org/languages/northeuralex-deu">Lexibank</a></li>
<li><a href="https://phoible.org/languages/stan1295">Phoible</a></li>
<li><a href="https://en.wikipedia.org/wiki/German_language">Wikipedia on German</a></li>
<li><a href="http://www.language-archives.org/language/deu">OLAC</a></li>
<li><a href="https://d-place.org/society/CCMCstan1295">D-Place</a></li>
<li><a href="https://lapsyd.huma-num.fr/lapsyd/index.php?data=view&code=99">LAPSyD</a></li>
<li><a href="https://huggingface.co/models?language=de&sort=trending&search=german">Hugging Face</a></li>
<li><a href="https://en.wikisource.org/wiki/An_Etymological_Dictionary_of_the_German_Language">WikiBook</a></li>
<li><a href="https://iecor.clld.org/languages/german">IECore</a></li>
<li><a href="https://glottolog.org/resource/languoid/id/stan1295">Glottolog</a></li>
</ul>

% endif

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    <div class="well well-small">
        <h3>Macroarea</h3>
        <p>${h.link(req, ctx.macroarea_obj)}</p>
    </div>
    ${util.language_meta()}
</%def>
