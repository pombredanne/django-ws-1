Ext.define('WS.view.layout.Main', {
    extend: 'Ext.container.Viewport',
    alias: 'widget.main',

    cls: 'x-main',
    autoScroll: true,
    layout : {
        type : 'border',
        padding: '0 5 5 5' // pad the layout from the window edges
    },

    initComponent : function() {

        this.items = [{
                xtype: 'header',
                region: 'north'
            },{
                id: 'dashboard',
                xtype: 'dashboard',
                region: 'center',
                split: true,
            },{
                region: 'west',
                html: 'aquivalasidebar',
                collapsible: true,
                split: true,
            }];

        this.callParent(arguments);
    }

});

