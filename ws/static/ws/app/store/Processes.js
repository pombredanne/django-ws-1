Ext.define('WS.store.Processes', {
    extend: 'Ext.data.Store',
    model: 'WS.model.Process',
    autoLoad: false,

    proxy: {
        type: 'ajax',
        api: {
            read: '/ws/processlaunchers.json',
            update: '/static/ws/data/updateTasks.json'
        },
        reader: {
            type: 'json',
            root: 'processlaunchers',
            successProperty: 'success'
        }
    }
});
