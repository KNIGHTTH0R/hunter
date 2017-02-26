// ==UserScript==
// @id iitc-plugin-ingress-guard-zoom@hunter
// @name IITC plugin: Ingress Guardian Zoom
// @category Layer
// @version 0.0.1.20161003.4825
// @namespace https://github.com/jonatkins/ingress-intel-total-conversion
// @description Show achievements on the map.
// @include https://*.ingress.com/intel*
// @include http://*.ingress.com/intel*
// @match https://*.ingress.com/intel*
// @match http://*.ingress.com/intel*
// @include https://*.ingress.com/mission/*
// @include http://*.ingress.com/mission/*
// @match https://*.ingress.com/mission/*
// @match http://*.ingress.com/mission/*
// @grant none
// ==/UserScript==
function wrapper(plugin_info) {
    // ensure plugin framework is there, even if iitc is not yet loaded
    if (typeof window.plugin !== 'function') window.plugin = function() {};
    //PLUGIN AUTHORS: writing a plugin outside of the IITC build environment? if so, delete these lines!!
    //(leaving them in place might break the 'About IITC' page or break update checks)
    plugin_info.buildName = 'iitc';
    plugin_info.dateTimeVersion = '20162912.6608';
    plugin_info.pluginId = 'iitc-plugin-ingress-guard-zoom';
    //END PLUGIN AUTHORS NOTE
    // PLUGIN START ////////////////////////////////////////////////////////
    // use own namespace for plugin
    window.plugin.ingressGuardZoom = function() {};

    var setup = function() {
        plugin.ingressGuardZoom.Zoom = new L.LayerGroup();
        window.addLayerGroup("[IG] Zoom", plugin.ingressGuardZoom.Zoom, false);
        if (map.hasLayer(plugin.ingressGuardZoom.Zoom)) {
            window.getDataZoomForMapZoom = function(zoom) {return 15};
        }
    }
    // PLUGIN END //////////////////////////////////////////////////////////
    setup.info = plugin_info; //add the script info data to the function as a property
    if (!window.bootPlugins) window.bootPlugins = [];
    window.bootPlugins.push(setup);
    // if IITC has already booted, immediately run the 'setup' function
    if (window.iitcLoaded && typeof setup === 'function') setup();
} // wrapper end
// inject code into site context
var script = document.createElement('script');
var info = {};
if (typeof GM_info !== 'undefined' && GM_info && GM_info.script) info.script = {
    version: GM_info.script.version,
    name: GM_info.script.name,
    description: GM_info.script.description
};
script.appendChild(document.createTextNode('(' + wrapper + ')(' + JSON.stringify(info) + ');'));
(document.body || document.head || document.documentElement).appendChild(script);