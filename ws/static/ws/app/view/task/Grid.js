Ext.define('WS.view.task.Grid' ,{
    extend: 'Ext.grid.Panel',
    alias : 'widget.taskgrid',
    store: 'Tasks',

    initComponent: function() {
        this.columns = [
            {header: 'Task',  dataIndex: 'task',  flex: 1},
            {header: 'Process', dataIndex: 'process', flex: 1},
            {header: 'Process type', dataIndex: 'process_type', flex: 1},
            {header: 'Priority', dataIndex: 'priority', flex: 1},
            {header: 'Date', dataIndex: 'date', flex: 1},
            {header: 'Status', dataIndex: 'status', flex: 1},
            {xtype:'actioncolumn', 
                width: 70,
                items: [{
                    icon: '/static/ws/images/edit.png',  // Use a URL in the icon config
                    tooltip: 'View',
                    handler: this.viewTask
                }]
            },
        ];

        this.callParent(arguments);
    },

    viewTask: function(grid, rowIndex, colIndex) {
        var record = grid.getStore().getAt(rowIndex);
        alert("View " + record.get('taskid')+' '+record.get('task'));
    },
});
