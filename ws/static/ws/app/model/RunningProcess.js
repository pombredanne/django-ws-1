Ext.define('WS.model.RunningProcess', {
    extend: 'Ext.data.Model',
    fields: ['id', 'title', 'type', 'creationTime', 'status'],

    proxy: {
        type: 'ajax',
        api: {
            read: '/ws/runningprocesses.json',
            update: '/static/ws/data/updateTasks.json'
        },
        reader: {
            type: 'json',
            root: 'runningprocesses',
            successProperty: 'success'
        }
    },
});
