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
        this.addEvents('auth_required', 'authenticated');

        this.viewport = Ext.create('WS.view.layout.Viewport', {
            id: 'viewport',
        });

        var authController = this.getController('Auth');
        authController.getUserInfo();
    },

});
