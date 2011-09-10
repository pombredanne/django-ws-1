Ext.define('WS.view.task.View', {
    extend: 'Ext.panel.Panel',
    alias : 'widget.taskview',

    title : 'View task',
    layout: 'fit',

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
                action: 'cancel'
            }
        ];

        this.callParent(arguments);
    }
});
