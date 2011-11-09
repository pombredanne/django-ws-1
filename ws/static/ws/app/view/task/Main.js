Ext.define('WS.view.task.Main', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.tasksmain',
    autoScroll: true,
    title: 'Tasks',
    refreshable: true,

    initComponent: function() {
        this.items = [{
            xtype: 'grid',
            store: 'Tasks',
            columns: [
                Ext.create('Ext.grid.RowNumberer'),
                {header: 'Task',  dataIndex: 'task',  flex: 1},
                //{header: 'User',  dataIndex: 'user',  flex: 1},
                {header: 'User',  xtype: 'templatecolumn', tpl:'TODO', flex: 1},
                {header: 'Process', dataIndex: 'process', flex: 1},
                {header: 'Workflow', dataIndex: 'workflow', flex: 1},
                //{header: 'Priority', dataIndex: 'priority', flex: 1},
                {header: 'Priority',  xtype: 'templatecolumn', tpl:'TODO', flex: 1},
                //{header: 'Date', dataIndex: 'date', flex: 1},
                {header: 'Date',  xtype: 'templatecolumn', tpl:'TODO', flex: 1},
                {header: 'State', dataIndex: 'state', flex: 1, renderer: this.statusRenderer},
                {header: 'Result', dataIndex: 'result', flex: 1},
                {header: 'Info required', dataIndex: 'info_required', flex: 1},
            ],
            dockedItems: [{
                xtype: 'pagingtoolbar',
                store: 'Tasks',
                dock: 'bottom',
                displayInfo: true,
            }],
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

    doRefresh: function() {
        var grid = this.down('gridpanel');
        grid.store.load();
    },
});
