Ext.define('WS.view.layout.DashboardSidebar', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.dashboardsidebar',
    items: [{
        xtype: 'fieldset',
        title: 'Add portlets',
        items: [{
            xtype: 'button',
            text: 'Tasks',
            action: 'taskPortlet',
        },{
            xtype: 'button',
            text: 'My tasks',
            action: 'myTasks'
        },{
            xtype: 'button',
            text: 'Process Starter',
            action: 'startProcess',
        },{
            xtype: 'button',
            text: 'Processes',
            action: 'processes',
        }],
    }],
});

