Ext.define('WS.view.process.ProcessDetail', {
    extend: 'Ext.tab.Panel',
    alias: 'widget.processdetail',
    autoScroll: true,
    height: 500,
    layout: 'fit',

    config: {
        pk: undefined,
        type: undefined,
    },

    initComponent: function() {
        this.items = [{
            title: 'Overview',
            items: [{
                tpl: Ext.create('Ext.Template',[
                    '<p><b>Process</b>: {pk}</p>',
                    '<p><b>Type</b>: {type}</p>',
                    '<p><b>Created</b>: TODO</p>',
                    '<p><b>Status</b>: TODO</p>',
                ]),
                data: {pk: this.getPk(), type: this.getType()},
            }],
        },{
            title: 'Tasks',
        },{
            title: 'Graph',
            items: [{
                xtype: 'image',
                src: '/ws/workflows/workflow_1.png',
            }],
        }];
        this.callParent(arguments);
    },
});

