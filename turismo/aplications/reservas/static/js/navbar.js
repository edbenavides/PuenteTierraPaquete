if (plugins.rdNavbar.length) {
    var aliaces, i, j, len, value, values, responsiveNavbar;

    aliaces = ["-", "-sm-", "-md-", "-lg-", "-xl-", "-xxl-"];
    values = [0, 576, 768, 992, 1200, 1600];
    responsiveNavbar = {};

    for (i = j = 0, len = values.length; j < len; i = ++j) {
        value = values[i];
        if (!responsiveNavbar[values[i]]) {
            responsiveNavbar[values[i]] = {};
        }
        if (plugins.rdNavbar.attr('data' + aliaces[i] + 'layout')) {
            responsiveNavbar[values[i]].layout = plugins.rdNavbar.attr('data' + aliaces[i] + 'layout');
        }
        if (plugins.rdNavbar.attr('data' + aliaces[i] + 'device-layout')) {
            responsiveNavbar[values[i]]['deviceLayout'] = plugins.rdNavbar.attr('data' + aliaces[i] + 'device-layout');
        }
        if (plugins.rdNavbar.attr('data' + aliaces[i] + 'hover-on')) {
            responsiveNavbar[values[i]]['focusOnHover'] = plugins.rdNavbar.attr('data' + aliaces[i] + 'hover-on') === 'true';
        }
        if (plugins.rdNavbar.attr('data' + aliaces[i] + 'auto-height')) {
            responsiveNavbar[values[i]]['autoHeight'] = plugins.rdNavbar.attr('data' + aliaces[i] + 'auto-height') === 'true';
        }

        if (isNoviBuilder) {
            responsiveNavbar[values[i]]['stickUp'] = false;
        } else if (plugins.rdNavbar.attr('data' + aliaces[i] + 'stick-up')) {
            responsiveNavbar[values[i]]['stickUp'] = plugins.rdNavbar.attr('data' + aliaces[i] + 'stick-up') === 'true';
        }

        if (plugins.rdNavbar.attr('data' + aliaces[i] + 'stick-up-offset')) {
            responsiveNavbar[values[i]]['stickUpOffset'] = plugins.rdNavbar.attr('data' + aliaces[i] + 'stick-up-offset');
        }
    }

    
    plugins.rdNavbar.RDNavbar({
        anchorNav:    !isNoviBuilder,
        stickUpClone: (plugins.rdNavbar.attr("data-stick-up-clone") && !isNoviBuilder) ? plugins.rdNavbar.attr("data-stick-up-clone") === 'true' : false,
        responsive:   responsiveNavbar,
        callbacks:    {
            onDropdownOver: function () {
                return !isNoviBuilder;
            },
        }
    });
    

    if (plugins.rdNavbar.attr("data-body-class")) {
        document.body.className += ' ' + plugins.rdNavbar.attr("data-body-class");
    }
    
    
}