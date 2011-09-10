Ext.define('WS.view.process.Starter', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.processstarter',

    title: 'Start new process',
    items: [{
            xtype: 'form',
            items: [{
                    id:'processescontainer',
                    xtype: 'fieldcontainer',
                    fieldLabel: 'Process type',
                }
            ]
    }],
    buttons : [
        {
            text: 'Start',
            action: 'start'
        }
    ],

    initComponent: function() {
        this.title_suggestion = 'Start new process';
        this.callParent(arguments);
    }
});
