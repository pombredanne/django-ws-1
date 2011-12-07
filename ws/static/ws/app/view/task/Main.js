Ext.define('WS.view.task.Main', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.tasksmain',
    autoScroll: true,
    title: 'Tasks',
    store: Ext.create('WS.store.Tasks', {
        autoLoad: true,
    }),

    lbar: [{
        xtype: 'fieldset',
        title: 'Actions',
        defaults: {
            xtype: 'button',
        },
        items: [{
            text: 'Start',
            action: 'starttask',
        },{
            text: 'End',
            action: 'endtask'
        },{
            text: 'Delegate',
            action: 'delegatetask',
        },{
            text: 'Add information',
            action: 'addinfotask',
        }],
    },{
        xtype: 'fieldset',
        title: 'Add Filters',
        items: [{
            xtype: 'combobox',
            fieldLabel: 'Column',
            store: [
                ['task','Name'],
                ['user','User'],
                ['process','Process'],
                ['workflow','Process type'],
                ['priority','Priority'],
                ['date','Date'],
                ['state','State'],
            ],
            typeAhead: 'true',
            },{
                xtype: 'combobox',
                fieldLabel: 'Value',
                displayField: 'task',
                valueField: 'pk',
                store: 'Tasks',
                queyModel: 'local',
                typeAhead: 'true',
        }],
    },{
        xtype: 'fieldset',
        title: 'Current Filters',
        html: 'TODO',
    }],

    initComponent: function() {
        this.items = [{
            xtype: 'taskgrid',
            store: this.store,
        },{
            id: 'taskdetail',
            region: 'south',
            height: '50%',
            collapsible: true,
            collapseMode: 'mini',
            preventHeader: true,
            split: true,
            items: [{
                title: 'Task details',
                html:'<p>Selecting a task in the grid show\'s detailed information here.</p>',
            }],
        }];
        this.callParent(arguments);
    },
});
