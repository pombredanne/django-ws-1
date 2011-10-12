Ext.define('WS.view.process.Running', {
    extend: 'WS.view.layout.Portlet',
    alias: 'widget.runningprocesses',
    autoScroll: true,
    title: 'Running processes',
    refreshable: true,
    fullscreen: true,
    fullscreenTarget: 'processes',

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
