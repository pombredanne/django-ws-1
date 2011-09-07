Ext.define('WS.view.auth.Login', {
    extend: 'Ext.window.Window',
    alias: 'widget.login',
    layout: 'fit',
    frame: true,
    title: 'Login',
    cls: 'x-login',

    initComponent: function() {
        this.items = [{
            xtype: 'form',
            url:'/ws/login',
            items: [{
                    xtype: 'textfield',
                    name : 'username',
                    fieldLabel: 'User'
                }, {
                    xtype: 'textfield',
                    inputType: 'password',
                    name : 'password',
                    fieldLabel: 'Password'
                }]
        }];

        this.buttons = [
            {
                text: 'Login',
                action: 'login'
            }];

        this.callParent(arguments);
    }
});
