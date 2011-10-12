Ext.define('WS.view.process.Main', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.processmain',
    autoScroll: true,
    title: 'Running processes',
    refreshable: true,

    initComponent: function() {
        this.items = [{
            xtype: 'grid',
            store: 'RunningProcesses',
            columns: [
                Ext.create('Ext.grid.RowNumberer'),
                {header: 'Process', dataIndex: 'title', flex: 1},
                {header: 'Type', dataIndex: 'type', flex: 1},
                {header: 'Created', dataIndex: 'creationTime', flex: 1},
                {header: 'Status', dataIndex: 'status', flex: 1},
            ],
            dockedItems: [{
                xtype: 'pagingtoolbar',
                store: 'RunningProcesses',
                dock: 'bottom',
                displayInfo: true,
            }],
        }];
        this.callParent(arguments);
    },

    doRefresh: function() {
        var grid = this.down('gridpanel');
        grid.store.load();
    },
});
