Ext.define('WS.view.process.Main', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.processmain',
    autoScroll: true,
    title: 'Processes',
    layout: {
        type: 'border',
        padding: 0
    },

    initComponent: function() {
        this.store = Ext.create('WS.store.Processes', {
            autoLoad: true,
        });
        this.items = [{
            xtype: 'processgrid',
            region: 'center',
            store: this.store,
        },{
            id: 'processdetail',
            region: 'south',
            height: '50%',
            collapsible: true,
            collapseMode: 'mini',
            preventHeader: true,
            split: true,
            items: [{
                title: 'Process details',
                html:'<p>Selecting a process in the grid show\'s detailed information here.</p>',
            }],
        }];
        this.callParent(arguments);
    },
});
