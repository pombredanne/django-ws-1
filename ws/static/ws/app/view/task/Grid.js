Ext.define('WS.view.task.Grid', {
    extend: 'WS.view.layout.Portlet',
    alias: 'widget.taskgrid',
    autoScroll: true,
    title: 'Tasks',
    items:[{
        xtype: 'grid',
        store: 'Tasks',
        columns: [
            {header: 'Task',  dataIndex: 'task',  flex: 1},
            {header: 'Process', dataIndex: 'process', flex: 1},
            {header: 'Process type', dataIndex: 'process_type', flex: 1},
            {header: 'Priority', dataIndex: 'priority', flex: 1},
            {header: 'Date', dataIndex: 'date', flex: 1},
            {header: 'Status', dataIndex: 'status', flex: 1, renderer: this.statusRenderer},
            {xtype:'actioncolumn', 
                width: 70,
                items: [{
                    icon: '/static/ws/images/edit.png',  // Use a URL in the icon config
                    tooltip: 'View',
                    handler: this.viewTask
                }]
            },
        ],
    }],

    initComponent: function() {
        this.callParent(arguments);
        grid = this.down('gridpanel');
        this.interval = setInterval(function(){
            console.log("refresh tasks");
            grid.store.load();
        }, 10000);
    },

    viewTask: function(grid, rowIndex, colIndex) {
        var record = grid.getStore().getAt(rowIndex);
        alert("View " + record.get('taskid')+' '+record.get('task'));
    },

    statusRenderer: function(value, metadata, record, rowIndex, colIndex, store, view) {
        // set td class same as value
        metadata["tdCls"]= value;
        return value;
    }
});
