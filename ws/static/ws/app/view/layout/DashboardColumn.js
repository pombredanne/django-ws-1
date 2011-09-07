Ext.define('WS.view.layout.DashboardColumn', {
    extend: 'Ext.container.Container',
    alias: 'widget.dashboardcolumn',
    layout: {
        type: 'anchor'
    },
    defaultType: 'portlet',
    cls: 'x-dashboard-column',
    autoHeight: true
});
