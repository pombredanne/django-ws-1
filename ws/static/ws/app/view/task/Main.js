Ext.define('WS.view.task.Main', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.tasksmain',
    autoScroll: true,
    title: 'Tasks',
    store: Ext.create('WS.store.Tasks', {
        autoLoad: true,
    }),

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
