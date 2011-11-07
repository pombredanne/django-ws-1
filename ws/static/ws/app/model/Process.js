Ext.define('WS.model.Process', {
    extend: 'Ext.data.Model',
    //fields: ['id', 'title', 'type', 'creationTime', 'status'],
    fields: ['pk', 'type'],

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
