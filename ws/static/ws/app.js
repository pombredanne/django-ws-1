Ext.application({
    name: 'WS',

    appFolder: '/static/ws/app',

    controllers: [
        'Layout',
        'Auth',
        'Tasks',
        'Process'
    ],

    launch: function() {
        Ext.create('WS.view.layout.Main', {
            id: 'viewport',
        });
    },
});
