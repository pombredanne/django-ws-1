Ext.define('WS.view.task.TaskDetail', {
    extend: 'Ext.tab.Panel',
    alias: 'widget.taskdetail',
    autoScroll: true,
    height: 500,
    layout: 'fit',

    pk: undefined,
    name: undefined,
    process: undefined,
    process_pk: undefined,
    workflow: undefined,
    workflow_pk: undefined,
    info_required: undefined,
    form_fields: undefined,

    initComponent: function() {
        this.overview = Ext.create('Ext.panel.Panel', {
            tpl: Ext.create('Ext.Template',[
                '<p><b>Task</b>: {pk}, {name}</p>',
                '<p><b>Process</b>: {process_pk}, {process}</p>',
                '<p><b>Type</b>:{workflow_pk}, {workflow}</p>',
                '<p><b>Created</b>: TODO</p>',
                '<p><b>Status</b>: TODO</p>',
            ]),
            data: {pk: this.pk, name: this.name,
                   process: this.process, process_pk: this.process_pk,
                   workflow: this.workflow, workflow_pk: this.workflow_pk},
        });

        this.image = Ext.create('Ext.Img', {
            src: '/ws/workflows/workflow_'+this.workflow_pk+'.png',
        });
        this.form = Ext.create('Ext.form.Panel', {
            items: this.form_fields,
            buttons: [{
                text: 'Send',
                action: 'send',
            }],
        });
        this.items = [{
            title: 'Data',
            items: [this.form],
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
        this.form.removeAll();
        this.form.add(data['form_fields']);
    }
});

