Ext.define('WS.view.layout.Menubar', {
    extend: 'Ext.toolbar.Toolbar',
    alias: 'widget.menubar',
    layout : 'hbox',

    cls: 'x-menu',

    user: undefined,

    initComponent : function() {
        // Implement a Container beforeLayout call from the layout to this Container
        this.items = [{
                text: 'Tasks',
                menu: {
                    xtype: 'menu',
                    items: [{
                        text: 'View all tasks',
                        action: 'taskPortlet',
                    },{
                        text: 'My tasks',
                        action: 'myTasksPortlet',
                    },{
                        text: 'Tasks of another user',
                    }]
                }
            },{
                text: 'Processes',
                menu: {
                    xtype: 'menu',
                    items: [{
                        text: 'Start new process',
                        action: 'startProcess',
                    },{
                        text: 'Processes',
                        action: 'processesPortlet',
                    },{
                        text: 'All processes',
                    }]
                }
            },'-',{
                xtype: 'buttongroup',
                itemId: 'viewChooser',
                defaults: {
                    text: null,
                    enableToggle: true,
                    toggleGroup: 'viewChooser',
                },
                items: [{
                    action: 'dashboard',
                    iconCls: 'dashboard',
                    tooltip: 'dashboard',
                },{
                    action: 'tasks',
                    iconCls: 'tasks',
                    tooltip: 'tasks',
                },{
                    action: 'processes',
                    iconCls: 'processes',
                    tooltip: 'processes',
                },{
                    action: 'messages',
                    iconCls: 'messages',
                    tooltip: 'messages',
                },{
                    action: 'administration',
                    iconCls: 'administration',
                    tooltip: 'administration',
                }],
            },'->',{
                text: this.user.get('username'),
                action: 'preferences'
            },{
                text: 'Logout',
                action: 'logout'
            }];

        this.callParent(arguments);
    }

});

