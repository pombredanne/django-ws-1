Ext.define('WS.view.process.New', {
    extend: 'WS.view.layout.Portlet',
    alias: 'widget.newprocess',
    title: 'New process',

    tpl: Ext.create('Ext.XTemplate',
        '<div class="process">',
        '<h3>{title}</h3>',
        '<p>{description}</p>',
        '<tpl if="enabled == true">',
        '<p>Enabled</p>',
        '</tpl>',
        '<tpl if="enabled == false">',
        '<p>Disabled</p>',
        '</tpl>',
        '</div>'
    )
});
