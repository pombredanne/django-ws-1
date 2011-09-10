Ext.define('WS.view.process.New', {
    extend: 'Ext.panel.Panel',
    alias : 'widget.newprocess',

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
    ),

    initComponent: function() {
        this.title_suggestion = 'New process';
        this.callParent(arguments);
    }
});
