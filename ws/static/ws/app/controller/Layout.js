Ext.define('WS.controller.Layout', {
    extend: 'Ext.app.Controller',
    views: [
        'layout.Portlet',
        'layout.PortletTaskGrid',
        'layout.DashboardColumn',
        'layout.Dashboard',
        'layout.Menubar',
        'layout.Header',
        'layout.Main',
    ],
});
