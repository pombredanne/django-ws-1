Ext.define('WS.view.layout.Menubar', {
    extend: 'Ext.toolbar.Toolbar',
    alias: 'widget.menubar',
    layout : 'hbox',

    cls: 'x-menu',

    initComponent : function() {
        // Implement a Container beforeLayout call from the layout to this Container

        this.items = [{
                text: 'Tasks',
                menu: {
                    xtype: 'menu',
                    items: [{
                        text: 'View all tasks',
                        action: 'viewAllTasks',
                    },{
                        text: 'My tasks',
                        action: 'myTasks',
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
                        text: 'Running processes',
                    },{
                        text: 'All processes',
                    }]
                }
            },{
                text: 'Preferences',
                action: 'preferences'
            },
            '->', //Begin with right aligned elements
            {
                text: 'Logout',
                action: 'logout'
            }];

        this.callParent(arguments);
    }

});

