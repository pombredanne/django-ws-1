Ext.define('WS.view.process.Running', {
    extend: 'WS.view.layout.Portlet',
    alias: 'widget.runningprocesses',
    autoScroll: true,
    title: 'Running processes',
    refreshable: true,
    items: [{
        xtype: 'grid',
        store: 'RunningProcesses',
        columns: [
            {header: 'Process', dataIndex: 'title', flex: 1},
            {header: 'Type', dataIndex: 'type', flex: 1},
            {header: 'Created', dataIndex: 'creationTime', flex: 1},
            {header: 'Status', dataIndex: 'status', flex: 1},
        ],
    }],

    doRefresh: function() {
        var grid = this.down('gridpanel');
        grid.store.load();
    },
});
