Ext.define('WS.controller.Auth', {
    extend: 'Ext.app.Controller',
    uses: ['Ext.util.Cookies'],
    models: ['User'],
    views: [
        'auth.Login',
    ],

    init: function() {
        this.control({
            'button[action=login]': {
                click: this.login
            },
            'button[action=logout]': {
                click: this.logout
            }
        });
        Ext.Ajax.on('beforerequest', this.ajax_csrf);

        this.on({
            authenticated: this.getUserInfo,
        })

        this.application.on({
            auth_required: this.auth_required,
            scope: this
        });
    },

    ajax_csrf: function(conn, options) {
        if (!(/^http:.*/.test(options.url) || /^https:.*/.test(options.url))) {
            if (typeof(options.headers) == "undefined") {
                options.headers = {'X-CSRFToken': Ext.util.Cookies.get('csrftoken')};
            } else {
                options.headers.extend({'X-CSRFToken': Ext.util.Cookies.get('csrftoken')});
            }                        
        }
    },

    login: function(button) {
        var form = button.up('form');
        var controller = this;
        form.submit({
            url:'/ws/login',
            method:'POST', 
            waitTitle:'Authenticating', 
            waitMsg:'Sending data...',
            success:function(form, action){ 
                controller.login_window.close();
                // Gather user information
                controller.getUserInfo();
            },

            failure: function(form, action) {
                switch (action.failureType) {
                    case Ext.form.action.Action.CLIENT_INVALID:
                        Ext.Msg.alert('Failure', 'Form fields may not be submitted with invalid values');
                        break;
                    case Ext.form.action.Action.CONNECT_FAILURE:
                        Ext.Msg.alert('Failure', 'Server communication failed');
                        break;
                    case Ext.form.action.Action.SERVER_INVALID:
                       Ext.Msg.alert('Failure', action.result.message);
               }
            }
        });
    },

    getUserInfo: function() {
        var controller = this;
        Ext.Ajax.request({
            url: '/ws/user.json',
            success: function(response) {
                data = Ext.JSON.decode(response.responseText)
                if (data['success'] == true) {
                    // Store user information in the application
                    controller.application.user = Ext.create('WS.model.User', {
                        pk: data['pk'],
                        username: data['username'],
                    });
                    controller.application.fireEvent('authenticated')
                } else {
                    controller.application.fireEvent('auth_required');
                }
            },
            failure: function(response) {
                console.log("error, presume unauthenticated");
            },
        });
    },

    logout: function(button) {
        var controller = this;
        Ext.Ajax.request({
            url: '/ws/logout',
            success: function(response) {
                controller.application.fireEvent('auth_required')
            },
        });
    },

    auth_required: function (){
        this.login_window = Ext.create('Ext.window.Window', {
            title: 'Login',
            resizable: false,
            closable: false,
            items : [{
                xtype:'authlogin',
            }],
        });
        this.login_window.show();
    },

});

