Ext.define('WS.view.layout.Viewport', {
    extend: 'Ext.container.Viewport',
    alias: 'widget.wsviewport',
    layout : {
        type : 'vbox',
        align: 'stretch',
    },

    items: [{
            flex: 1,
            id: 'ws-main',
            layout : {
                type : 'vbox',
                align: 'stretch',
            },
        },{
            xtype: 'statusbar',
            height: 20,
    }],

});
