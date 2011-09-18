Ext.define('WS.view.process.Starter', {
    extend: 'WS.view.layout.Portlet',
    alias: 'widget.processstarter',
    autoScroll: true,
    title: 'Start new process',

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
    ]
});
