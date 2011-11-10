Ext.define('WS.view.task.Portlet', {
    extend: 'WS.view.layout.Portlet',
    alias: 'widget.taskportlet',
    autoScroll: true,
    title: 'Tasks',
    refreshable: true,
    fullscreen: true,
    fullscreenTarget: 'tasks',

    initComponent: function() {
        this.store = Ext.create('WS.store.Tasks', {
            autoLoad: true,
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
