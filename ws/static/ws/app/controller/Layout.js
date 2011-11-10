Ext.define('WS.controller.Layout', {
    extend: 'Ext.app.Controller',
    views: [
        'layout.Portlet',
        'layout.DashboardColumn',
        'layout.Dashboard',
        'layout.DashboardDropZone',
        'layout.DashboardSidebar',
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
            'menubar menuitem[action=taskPortlet]': {
                click: this.taskPortlet
            },
            'menubar menuitem[action=startProcess]': {
                click: this.startProcess
            },
            'menubar menuitem[action=processes]': {
                click: this.processes
            },
            '#viewChooser button': {
                toggle: this.changeView,
            },
            'dashboardsidebar button[action=processes]': {
                click: this.processes
            },
            'dashboardsidebar button[action=taskPortlet]': {
                click: this.taskPortlet
            },
            'portlet tool[action=fullscreen]': {
                click: this.goToFullscreen
            }
        });
        this.on('new_widget', this.new_widget);
    },

    loadColumns: function(main, component) {
        if (component.alias == 'widget.dashboard') {
            //Create columns
            var i,
                num_columns = 2;
            for (i=1; i<=num_columns; i++) {
                component.add({
                    id: "col"+i,
                });
            };
            //Create portlets
            portlet = Ext.create('WS.view.process.Portlet');
            component.items.items[0].add(portlet);

            portlet = Ext.create('WS.view.task.Portlet');
            component.items.items[0].add(portlet);

            //portlet = Ext.create('WS.view.process.Starter');
            //component.items.items[1].add(portlet);

            portlet = Ext.create('WS.view.layout.Portlet', {
                html: "kaixo3",
            });
            component.items.items[1].add(portlet);
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

    taskPortlet: function(button) {
        var view = Ext.create('WS.view.task.Portlet');
        this.fireEvent('new_widget',view);
    },

    startProcess: function(button) {
        var view = Ext.create('WS.view.process.Starter');
        this.fireEvent('new_widget',view);
    },

    processes: function(button) {
        console.log("process portlet");
        var view = Ext.create('WS.view.process.Portlet');
        this.fireEvent('new_widget',view);
    },

    changeView: function(button, pressed) {
        if (pressed) {
            var center = Ext.ComponentManager.get('app-center'),
                sidebar = Ext.ComponentManager.get('app-sidebar');
            center.setLoading(true);
            center.removeAll();
            sidebar.setLoading(true);
            sidebar.removeAll();
            var view, side;
            switch(button.action) {
                case 'dashboard':
                    var view = Ext.create('WS.view.layout.Dashboard'),
                        side = Ext.create('WS.view.layout.DashboardSidebar');
                    break;
                case 'tasks':
                    var view = Ext.create('WS.view.task.Main'),
                        side = Ext.create('WS.view.task.MainSidebar');
                    break;
                case 'processes':
                    var view = Ext.create('WS.view.process.Main'),
                        side = Ext.create('WS.view.process.MainSidebar');
                    break;
                default:
                    var view = Ext.create("Ext.panel.Panel", {html: "TODO"}),
                        side = Ext.create("Ext.panel.Panel", {html: "TODO"});
            }
            center.add(view);
            center.setLoading(false);
            sidebar.add(side);
            sidebar.setLoading(false);
        };
    },
    goToFullscreen: function(tool) {
        var portlet = tool.up('portlet'),
            button = {
                action: portlet.fullscreenTarget,
            }
        this.changeView(button,true);
    },
});
