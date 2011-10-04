Ext.define('WS.view.layout.DashboardSidebar', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.dashboardsidebar',
    items: [{
        xtype: 'button',
        text: 'All tasks',
        action: 'viewAllTasks',
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
        text: 'Running Processes',
        action: 'runningProcesses',
    }],
});

