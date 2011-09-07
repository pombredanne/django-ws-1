Ext.define('WS.view.auth.Login', {
    extend: 'Ext.panel.Panel',
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
            },
            {
                text: 'Cancel',
                scope: this,
                handler: this.close
            }];

        this.callParent(arguments);
    }
});
