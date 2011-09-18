Ext.define('WS.view.process.Running', {
    extend: 'WS.view.layout.Portlet',
    alias: 'widget.runningprocesses',
    autoScroll: true,
    title: 'Running processes',
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

    initComponent: function() {
        this.callParent(arguments);
        grid = this.down('gridpanel');
        this.interval = setInterval(function(){
            console.log("refresh running processes");
            grid.store.load();
        }, 10000);
    },
});
