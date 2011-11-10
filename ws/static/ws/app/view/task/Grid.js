Ext.define('WS.view.task.Grid', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.taskgrid',
    layout: 'fit',

    initComponent: function() {
        if (! this.store) {
            this.store = Ext.create('WS.store.Tasks');
        }
        this.columns = [
            Ext.create('Ext.grid.RowNumberer'),
            {header: 'Task',  dataIndex: 'task',  flex: 1},
            //{header: 'User',  dataIndex: 'user',  flex: 1},
            {header: 'Process', dataIndex: 'process', flex: 1},
            {header: 'Workflow', dataIndex: 'workflow', flex: 1},
            //{header: 'Priority', dataIndex: 'priority', flex: 1},
            //{header: 'Date', dataIndex: 'date', flex: 1},
            {header: 'State', dataIndex: 'state', flex: 1, renderer: this.statusRenderer},
            {header: 'Result', dataIndex: 'result', flex: 1},
            {header: 'Info required', dataIndex: 'info_required', flex: 1},
            {xtype:'actioncolumn', 
                width: 70,
                items: [{
                    icon: '/static/ws/images/activate.png',  // Use a URL in the icon config
                    tooltip: 'Activate',
                    handler: this.activateTask
                },{
                    icon: '/static/ws/images/accept.png',  // Use a URL in the icon config
                    tooltip: 'Complete',
                    handler: this.completeTask
                }]
            },
        ];
        this.dockedItems = [{
            xtype: 'pagingtoolbar',
            store: this.store,
            dock: 'bottom',
            displayInfo: true,
        }];
        this.callParent(arguments);
    },

    activateTask: function(grid, rowIndex, colIndex) {
        var record = grid.getStore().getAt(rowIndex);
        alert("Activate " + record.get('taskid')+' '+record.get('task'));
    },

    completeTask: function(grid, rowIndex, colIndex) {
        var record = grid.getStore().getAt(rowIndex);
        alert("Complete " + record.get('taskid')+' '+record.get('task'));
    },

    statusRenderer: function(value, metadata, record, rowIndex, colIndex, store, view) {
        // set td class same as value
        metadata["tdCls"]= value;
        return value;
    },
});
