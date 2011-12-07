Ext.define('WS.view.layout.Main', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.main',

    cls: 'x-main',
    autoScroll: true,
    height: 500,
    layout : {
        type : 'border',
        padding: '0 5 5 5' // pad the layout from the window edges
    },

    user: undefined,

    initComponent : function() {
        this.items = [{
                xtype: 'menubar',
                region: 'north',
                user: this.user
            },{
                id: 'app-center',
                region: 'center',
                layout: 'fit',
                items: [{
                    html: 'erdialdea',
                }],
        }];
        this.callParent(arguments);
    },
});
