Ext.define('WS.store.Tasks', {
    extend: 'Ext.data.Store',
    model: 'WS.model.Task',
    autoLoad: false,
    pageSize: 10,
    remoteFilter: true,
});
