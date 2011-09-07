Ext.define('WS.view.layout.PortletTaskGrid', {
    extend: 'WS.view.layout.Portlet',
    alias: 'widget.portlettaskgrid',
    title : 'Tasks',

    initComponent: function() {
        this.items = [Ext.create('WS.view.task.Grid')]
        this.callParent(arguments);
    }
});
