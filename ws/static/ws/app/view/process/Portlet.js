Ext.define('WS.view.process.Portlet', {
    extend: 'WS.view.layout.Portlet',
    alias: 'widget.processesportlet',
    autoScroll: true,
    title: 'Processes',
    refreshable: true,
    fullscreen: true,
    fullscreenTarget: 'processes',

    initComponent: function() {
        this.store = Ext.create('WS.store.Processes', {
            autoLoad: true,
        });
        this.items = [{
            xtype: 'processgrid',
            store: this.store,
        }];
        this.callParent(arguments);
    },

    doRefresh: function() {
        var grid = this.down('gridpanel');
        grid.store.load();
    },
});
