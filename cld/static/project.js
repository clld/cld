GLOTTOLOG3 = {};

GLOTTOLOG3.style = function(feature) {
    return {
            'color': '#000',
            'weight': 1,
            'opacity': 0.3,
            'fillOpacity': 0.3,
            'fillColor': '#222222'
    }
};

GLOTTOLOG3.highlight = undefined;

GLOTTOLOG3.highlightMacroarea = function(e) {
    var layer = e.target,
        style = GLOTTOLOG3.style(layer.feature);
    if (GLOTTOLOG3.highlight) {
        GLOTTOLOG3.highlight.setStyle(GLOTTOLOG3.style(GLOTTOLOG3.highlight.feature));
    }
    GLOTTOLOG3.highlight = layer;
    style.weight = 3;
    style.color = '#f00';
    style.opacity = 0.8;
    layer.setStyle(style);
    //CLLD.mapShowInfoWindow('map', layer, layer.feature.properties.latlng);
    return false;
};

CLLD.LayerOptions.macroareas = {
    style: GLOTTOLOG3.style,
    onEachFeature: function(feature, layer) {
        layer.bindTooltip(feature.properties.label);
        layer.bindPopup(feature.properties.description);
        layer.on({mouseover: GLOTTOLOG3.highlightMacroarea});
        //((CLLD.Maps.map.marker_map[feature.properties.id] = layer;

        // Create a self-invoking function that passes in the layer
        // and the properties associated with this particular record.
        //(function(layer, properties) {
        //    layer.on('click', function(e) {
        //        CLLD.mapShowInfoWindow('map', layer, e.latlng);
        //    });
            // Close the "anonymous" wrapper function, and call it while passing
            // in the variables necessary to make the events work the way we want.
        //})(layer, feature.properties);
    }
};
