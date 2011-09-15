Ext.define('WS.view.process.Starter', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.processstarter',

    items: [{
            xtype: 'form',
            items: [{
                xtype: 'fieldset',
                title: 'Process type',
                items: [{
                        id:'processescontainer',
                        xtype: 'fieldcontainer',
                        fieldLabel: 'Process type',
                }],
            },{
                xtype: 'fieldset',
                title: 'Process details',
                hidden: true,
            }],
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
