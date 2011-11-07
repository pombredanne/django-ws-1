Ext.define('WS.view.process.Portlet', {
    extend: 'WS.view.layout.Portlet',
    alias: 'widget.processesportlet',
    autoScroll: true,
    title: 'Processes',
    refreshable: true,
    fullscreen: true,
    fullscreenTarget: 'processes',

    initComponent: function() {
        this.items = [{
            xtype: 'grid',
            store: 'Processes',
            columns: [
                Ext.create('Ext.grid.RowNumberer'),
                {header: 'pk', dataIndex: 'pk', flex: 1},
                //{header: 'Process', dataIndex: 'title', flex: 1},
                {header: 'Process',  xtype: 'templatecolumn', tpl:'TODO', flex: 1},
                {header: 'Type', dataIndex: 'type', flex: 1},
                //{header: 'Created', dataIndex: 'creationTime', flex: 1},
                {header: 'Created',  xtype: 'templatecolumn', tpl:'TODO', flex: 1},
                //{header: 'Status', dataIndex: 'status', flex: 1},
                {header: 'Status',  xtype: 'templatecolumn', tpl:'TODO', flex: 1},
            ],
            dockedItems: [{
                xtype: 'pagingtoolbar',
                store: 'Processes',
                dock: 'bottom',
                displayInfo: true,
            }],
        }];
        this.callParent(arguments);
    },

    doRefresh: function() {
        var grid = this.down('gridpanel');
        grid.store.load();
    },
});
