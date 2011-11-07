Ext.define('WS.store.Workflows', {
    extend: 'Ext.data.Store',
    model: 'WS.model.Workflow',
    autoLoad: false,
    pageSize: 10,
});
