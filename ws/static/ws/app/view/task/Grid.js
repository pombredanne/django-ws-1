Ext.define('WS.view.task.Grid' ,{
    extend: 'Ext.grid.Panel',
    alias : 'widget.taskgrid',
    store: 'Tasks',

    initComponent: function() {
        this.columns = [
            {header: 'Task',  dataIndex: 'task',  flex: 1},
            {header: 'Process', dataIndex: 'process', flex: 1},
            {header: 'Process type', dataIndex: 'process_type', flex: 1},
            {header: 'Priority', dataIndex: 'priority', flex: 1}
        ];

        this.callParent(arguments);
    }
});
