Ext.define('WS.view.process.Starter', {
    extend: 'Ext.panel.Panel',
    alias : 'widget.processstarter',

    title : 'Start new process',

    initComponent: function() {
        this.items = [
            {
                xtype: 'form',
                items: [{
                        id:'processescontainer',
                        xtype: 'fieldcontainer',
                        fieldLabel: 'Process type',
                    }
                ]
            }
        ];

        this.buttons = [
            {
                text: 'Start',
                action: 'start'
            }
        ];

        this.callParent(arguments);
    }
});
