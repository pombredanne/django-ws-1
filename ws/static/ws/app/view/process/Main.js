Ext.define('WS.view.process.Main', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.processmain',
    autoScroll: true,
    title: 'Processes',
    refreshable: true,
    layout: {
        type: 'border',
        padding: 0
    },

    initComponent: function() {
        this.items = [{
            xtype: 'grid',
            region: 'center',
            layout: 'fit',
            store: 'Processes',
            columns: [
                Ext.create('Ext.grid.RowNumberer'),
                {header: 'Process', dataIndex: 'name', flex: 1},
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
        },{
            id: 'processdetail',
            region: 'south',
            height: '50%',
            collapsible: true,
            collapseMode: 'mini',
            split: true,
            items: [{
                title: 'Process details',
                html:'<p>Selecting a process in the grid show\'s detailed information here.</p>',
            }],
        }];
        this.callParent(arguments);
    },

    doRefresh: function() {
        var grid = this.down('gridpanel');
        grid.store.load();
    },
});
