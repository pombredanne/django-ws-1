Ext.define('WS.controller.Layout', {
    extend: 'Ext.app.Controller',
    views: [
        'layout.Portlet',
        'layout.DashboardColumn',
        'layout.Dashboard',
        'layout.DashboardDropZone',
        'layout.Menubar',
        'layout.Header',
        'layout.Main',
        'layout.Statusbar',
    ],

    init: function() {
        this.addEvents('new_widget');
        this.control({
            'main': {
                add: this.loadColumns,
            },
            'menubar menuitem[action=viewAllTasks]': {
                click: this.viewAllTasks
            },
            'menubar menuitem[action=startProcess]': {
                click: this.startProcess
            },
            'menubar menuitem[action=runningProcesses]': {
                click: this.runningProcesses
            },
            'menubar button[action=preferences]': {
                click: this.preferences
            }
        });
        this.on('new_widget', this.new_widget);
    },

    loadColumns: function(main, component) {
        if (component.alias == 'widget.dashboard') {
            //Create columns
            var i,
                num_columns = 3;
            for (i=1; i<=num_columns; i++) {
                component.add({
                    id: "col"+i,
                });
            };
            //Create portlets
            portlet = Ext.create('WS.view.process.Running');
            component.items.items[0].add(portlet);

            portlet = Ext.create('WS.view.task.Grid');
            component.items.items[0].add(portlet);

            portlet = Ext.create('WS.view.process.Starter');
            component.items.items[1].add(portlet);

            portlet = Ext.create('WS.view.layout.Portlet', {
                html: "kaixo3",
            });
            component.items.items[2].add(portlet);
        }
        return true;
    },

    // Add the new widgeth to the dashboard column with less elements
    new_widget: function(portlet) {
        var dashboard = Ext.ComponentManager.get('dashboard'),
            target_column = -1,
            target_height = 999999,
            column_idx, column, column_size;
        for (column_idx=0; column_idx<dashboard.items.length ; column_idx++) {
            // The second 'items' required, not sure why
            column = dashboard.items.items[column_idx];
            column_size = column.getSize();
            if (column_size['height'] < target_height) {
                target_height = column_size['height'];
                target_column = column;
            }
        }
        target_column.add(portlet);
    },

    viewAllTasks: function(button) {
        var view = Ext.create('WS.view.task.Grid');
        this.fireEvent('new_widget',view);
    },

    startProcess: function(button) {
        var view = Ext.create('WS.view.process.Starter');
        this.fireEvent('new_widget',view);
    },

    runningProcesses: function(button) {
        var view = Ext.create('WS.view.process.Running');
        this.fireEvent('new_widget',view);
    },

    preferences: function(button) {
        var view = Ext.create('Ext.panel.Panel', {
            html: "Kaixo!"
        });
        this.fireEvent('new_widget',view);
    }
});
