Ext.define('WS.view.layout.Main', {
    extend: 'Ext.container.Viewport',
    alias: 'widget.main',

    cls: 'x-main',
    autoScroll: true,
    layout : {
        type : 'border',
        padding: '0 5 5 5' // pad the layout from the window edges
    },
    items: [{
            xtype: 'header',
            region: 'north'
        },{
            id: 'app-center',
            region: 'center',
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
        /*
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
        */
        },{
            xtype: 'statusbar',
            region: 'south',
    }],

});

