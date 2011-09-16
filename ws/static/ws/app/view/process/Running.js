Ext.define('WS.view.process.Running', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.runningprocesses',
    store: 'RunningProcesses',
    autoScroll: true,

    initComponent: function() {
        this.title_suggestion = 'Running processes';
        this.columns = [
            {header: 'Process', dataIndex: 'title', flex: 1},
            {header: 'Type', dataIndex: 'type', flex: 1},
            {header: 'Created', dataIndex: 'creationTime', flex: 1},
            {header: 'Status', dataIndex: 'status', flex: 1},
        ];
        this.callParent(arguments);
    }
});
