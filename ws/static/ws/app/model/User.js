Ext.define('WS.model.User', {
    extend: 'Ext.data.Model',
    fields: ['pk','username'],
    proxy: {
        type: 'ajax',
        api: {
            read: '/ws/users.json',
            update: '/static/ws/data/updateTasks.json'
        },
        reader: {
            type: 'json',
            root: 'rows',
        }
    }
});
