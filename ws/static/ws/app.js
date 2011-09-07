Ext.application({
    name: 'WS',

    appFolder: '/static/ws/app',

    controllers: [
        'Layout',
        'Auth',
        'Tasks'
    ],

    launch: function() {
        Ext.create('Ext.container.Viewport', {
            id: 'viewport',
            layout: 'fit',
            items: [
                {
                    //xtype: 'taskgrid',
                    //xtype: 'portlet',
                    //xtype: 'portlettaskview',
                    xtype: 'dashboard',
                    //xtype: 'login',
                }
            ]
        });
    },
});
