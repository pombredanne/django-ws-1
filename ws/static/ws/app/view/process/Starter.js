Ext.define('WS.view.process.Starter', {
    extend: 'Ext.panel.Panel',
    alias : 'widget.processstarter',

    title : 'Start new process',

    initComponent: function() {
        this.items = [
            {
                xtype: 'form',
                items: [{
                        xtype: 'fieldcontainer',
                        fieldLabel: 'Process',
                        defaultType: 'radiofield',
                        items:[{
                            boxLabel  : 'Tortilla de queso',
                            name      : 'process',
                            inputValue: '1',
                            id        : 'radio1'
                        }, {
                            boxLabel  : 'Flan',
                            name      : 'process',
                            inputValue: '2',
                            id        : 'radio2'
                        }, {
                            boxLabel  : 'Ensalada',
                            name      : 'process',
                            inputValue: '3',
                            id        : 'radio3'
                        }]
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
