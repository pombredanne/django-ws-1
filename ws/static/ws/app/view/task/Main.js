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
        }];
        this.callParent(arguments);
    },
});
