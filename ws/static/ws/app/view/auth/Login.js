Ext.define('WS.view.auth.Login', {
    extend: 'Ext.form.Panel',
    alias: 'widget.authlogin',
    layout: 'fit',
    frame: true,
    cls: 'x-login',

    initComponent: function() {
        this.items = [{
            xtype: 'textfield',
            name : 'username',
            fieldLabel: 'User'
        }, {
            xtype: 'textfield',
            inputType: 'password',
            name : 'password',
            fieldLabel: 'Password'
        }];

        this.buttons = [{
                text: 'Login',
                action: 'login'
            }];

        this.callParent(arguments);
    }
});
