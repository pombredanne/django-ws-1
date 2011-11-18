Ext.define('WS.model.Process', {
    extend: 'Ext.data.Model',
    fields: ['pk', 'name', 'workflow', 'workflow_pk', 'start_date', 'end_date', 'status'],

    proxy: {
        type: 'ajax',
        api: {
            read: '/ws/processes.json',
            update: '/static/ws/data/updateTasks.json'
        },
        reader: {
            type: 'json',
            root: 'rows',
        }
    }
});
