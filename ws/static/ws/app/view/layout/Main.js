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

    /*
    items: [{
            xtype: 'header',
            region: 'north'
        },{
            id: 'app-center',
            region: 'center',
            layout: 'fit',
            items: [{
                html: 'erdialdea',
            }],
        },{
            id: 'app-sidebar',
            region: 'west',
            preventHeader: true,
            collapsible: true,
            collapseMode: 'mini',
            split: true,
            items: [{
                html: 'sidebar',
            }],
        },{
            xtype: 'statusbar',
            region: 'south',
    }],
    */

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
            },{
                id: 'app-sidebar',
                region: 'west',
                preventHeader: true,
                collapsible: true,
                collapseMode: 'mini',
                split: true,
                items: [{
                    html: 'sidebar',
                }],
        }];
        this.callParent(arguments);
    },
});
