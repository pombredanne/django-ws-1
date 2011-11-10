Ext.define('WS.view.process.ProcessDetail', {
    extend: 'Ext.tab.Panel',
    alias: 'widget.processdetail',
    autoScroll: true,
    height: 500,
    layout: 'fit',

    pk: undefined,
    name: undefined,
    workflow: undefined,
    workflow_pk: undefined,

    initComponent: function() {
        this.store = Ext.create('WS.store.Tasks', {
            autoLoad: true,
            filters: [{
                property: 'process',
                value: this.pk,
            }],
        });

        this.overview = Ext.create('Ext.panel.Panel', {
            tpl: Ext.create('Ext.Template',[
                '<p><b>Process</b>: {pk}, {name}</p>',
                '<p><b>Type</b>:{workflow_pk}, {workflow}</p>',
                '<p><b>Created</b>: TODO</p>',
                '<p><b>Status</b>: TODO</p>',
            ]),
            data: {pk: this.pk, name: this.name, workflow: this.workflow, workflow_pk: this.workflow_pk},
        });

        this.image = Ext.create('Ext.Img', {
            src: '/ws/workflows/workflow_'+this.workflow_pk+'.png',
        });

        this.items = [{
            title: 'Tasks',
            items: [{
                xtype: 'taskgrid',
                store: this.store,
            }],
        }, {
            title: 'Overview',
            items: [this.overview],
        }, {
            title: 'Graph',
            items: [this.image],
        }];
        this.callParent(arguments);
    },

    reloadData: function(data) {
        this.overview.update(data);
        this.image.setSrc('/ws/workflows/workflow_'+data['workflow_pk']+'.png');
        this.store.clearFilter();
        this.store.filter([{
                property: 'process',
                value: data['pk'],
        }]);
    }
});

