Ext.define('WS.store.RunningProcesses', {
    extend: 'Ext.data.Store',
    model: 'WS.model.RunningProcess',
    autoLoad: false,
    pageSize: 10,
});
