Ext.define('WS.view.layout.Viewport', {
    extend: 'Ext.container.Viewport',
    alias: 'widget.wsviewport',
    layout : {
        type : 'vbox',
        align: 'stretch',
    },

    items: [{
            xtype: 'panel',
            height: 40,
            layout: 'hbox',
            items: [{
                 xtype: 'image',
                 src: '/static/logo.png',
                 heigth: 30,
            }]
        },{
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

    loadMain: function() {
        console.log("inside load main");
        var center = this.down('#app-center');
        center.add({html:'kaixo'});
    },

});
