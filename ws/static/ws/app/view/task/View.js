Ext.define('WS.view.task.View', {
    extend: 'Ext.window.Window',
    alias : 'widget.taskview',

    title : 'View task',
    layout: 'fit',
    autoShow: true,

    initComponent: function() {
        this.items = [
            {
                xtype: 'form',
                items: [{
                        xtype: 'textfield',
                        name : 'task',
                        fieldLabel: 'Tasks'
                    }, {
                        xtype: 'textfield',
                        name : 'process',
                        fieldLabel: 'Process'
                    }, {
                        xtype: 'textfield',
                        name : 'process',
                        fieldLabel: 'Process type'
                    }, {
                        xtype: 'textfield',
                        name : 'priority',
                        fieldLabel: 'Priority'
                    }
                ]
            }
        ];

        this.buttons = [
            {
                text: 'Save',
                action: 'save'
            },
            {
                text: 'Cancel',
                scope: this,
                handler: this.close
            }
        ];

        this.callParent(arguments);
    }
});
