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
        this.store = Ext.create('WS.store.Tasks', {
            autoLoad: true,
            filters: [{
                property: 'process',
                value: this.getPk(),
            }],
        });

        this.items = [{
            title: 'Tasks',
            items: [{
                xtype: 'taskgrid',
                store: this.store,
                layout: 'fit',
            }],
        },{
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
            title: 'Graph',
            items: [{
                xtype: 'image',
                src: '/ws/workflows/workflow_1.png',
            }],
        }];
        this.callParent(arguments);
    },
});

