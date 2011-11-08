Ext.define('WS.view.process.ProcessDetail', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.processdetail',
    autoScroll: true,
    height: 500,
    layout: {
        type: 'border',
        padding: '0 5 5 5'
    },

    config: {
        pk: undefined,
        type: undefined,
    },

    initComponent: function() {
        this.title = "Process: "+this.getPk();
        this.items = [{
            region: 'east',
            items: [{
                html: 'Process graph',
            }],
        },{
            region: 'center',
            items: [{
                tpl: Ext.create('Ext.Template',[
                    '<p><b>Process</b>: {pk}</p>',
                    '<p><b>Type</b>: {type}</p>',
                    '<p><b>Created</b>: TODO</p>',
                    '<p><b>Status</b>: TODO</p>',
                ]),
                data: {pk: this.getPk(), type: this.getType()},
            }],
        }];
        this.callParent(arguments);
    },
});

