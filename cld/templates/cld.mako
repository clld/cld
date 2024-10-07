<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="header">
    <div style="width: 100%; background-color: #fff6d5">
    <a href="${request.route_url('dataset')}">
        <img width="50%" src="${request.static_url('cld:static/header.png')}"/>
    </a>
    </div>
</%block>

${next.body()}
