Ext.define('WS.model.Task', {
    extend: 'Ext.data.Model',
    //fields: ['pk','task', 'user', 'process', 'process_type', 'priority', 'date', 'status'],
    fields: ['pk','task', 'process', 'workflow', 'state', 'result', 'info_required'],
    proxy: {
        type: 'ajax',
        api: {
            read: '/ws/tasks.json',
            update: '/static/ws/data/updateTasks.json'
        },
        reader: {
            type: 'json',
            root: 'rows',
        }
    }
});
