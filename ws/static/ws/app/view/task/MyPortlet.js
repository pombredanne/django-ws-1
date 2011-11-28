Ext.define('WS.view.task.MyPortlet', {
    extend: 'WS.view.layout.Portlet',
    alias: 'widget.mytaskportlet',
    autoScroll: true,
    title: 'My Tasks',
    refreshable: true,
    fullscreen: true,
    fullscreenTarget: 'tasks',

    initComponent: function() {
        this.store = Ext.create('WS.store.Tasks', {
            autoLoad: true,
            filters: [{
                property: 'user',
                value: '2',
            }]
        });
        this.items = [{
            xtype: 'taskgrid',
            store: this.store,
        }];
        this.callParent(arguments);
    },

    doRefresh: function() {
        var grid = this.down('gridpanel');
        grid.store.load();
    },
});
