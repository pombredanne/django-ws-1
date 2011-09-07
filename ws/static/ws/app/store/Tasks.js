Ext.define('WS.store.Tasks', {
    extend: 'Ext.data.Store',
    model: 'WS.model.Task',
    autoLoad: true,

    proxy: {
        type: 'ajax',
        api: {
            read: '/static/ws/data/tasks.json',
            update: '/static/ws/data/updateTasks.json'
        },
        reader: {
            type: 'json',
            root: 'tasks',
            successProperty: 'success'
        }
    }
});
