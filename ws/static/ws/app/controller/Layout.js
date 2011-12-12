Ext.define('WS.controller.Layout', {
    extend: 'Ext.app.Controller',
    views: [
        'layout.Dashboard',
        'layout.DashboardColumn',
        'layout.DashboardDropZone',
        'layout.Main',
        'layout.Menubar',
        'layout.Portlet',
        'layout.Statusbar',
        'layout.Viewport',
    ],

    init: function() {
        this.addEvents('new_widget');
        this.control({
            '#app-center': {
                add: this.loadColumns,
            },
            'menubar menuitem[action=taskPortlet]': {
                click: this.taskPortlet
            },
            'menubar menuitem[action=startProcess]': {
                click: this.startProcess
            },
            'menubar menuitem[action=processesPortlet]': {
                click: this.processes
            },
            '#viewChooser button': {
                toggle: this.chooseView,
            },
            'button[action=processesPortlet]': {
                click: this.processes
            },
            'button[action=myTaskPortlet]': {
                click: this.myTaskPortlet
            },
            'button[action=taskPortlet]': {
                click: this.taskPortlet
            },
            'button[action=startProcess]': {
                click: this.startProcess
            },
            'portlet tool[action=fullscreen]': {
                click: this.goToFullscreen
            }
        });
        this.on('new_widget', this.new_widget);
        this.application.on({
            authenticated: this.loadMain,
            auth_required: this.unloadMain,
            scope: this
        });
    },

    loadMain: function() {
        var wsmain = Ext.getCmp('ws-main');
        wsmain.removeAll();
        wsmain.add({
            xtype: 'main',
            flex: 1,
            user: this.application.user
        });
        this.changeView('dashboard');
    },

    unloadMain: function() {
        var wsmain = Ext.getCmp('ws-main');
        wsmain.removeAll();
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

    myTaskPortlet: function(button) {
        var view = Ext.create('WS.view.task.MyPortlet');
        this.fireEvent('new_widget',view);
    },

    startProcess: function(button) {
        var view = Ext.create('WS.view.process.PortletNew');
        this.fireEvent('new_widget',view);
    },

    processes: function(button) {
        var view = Ext.create('WS.view.process.Portlet');
        this.fireEvent('new_widget',view);
    },

    changeView: function(target) {
        var center = Ext.ComponentManager.get('app-center');
        center.setLoading(true);
        center.removeAll();
        var view;
        switch(target) {
            case 'dashboard':
                var view = Ext.create('WS.view.layout.Dashboard');
                break;
            case 'tasks':
                var view = Ext.create('WS.view.task.Main');
                break;
            case 'processes':
                var view = Ext.create('WS.view.process.Main');
                break;
            default:
                var view = Ext.create("Ext.panel.Panel", {html: "TODO"});
        }
        center.add(view);
        center.setLoading(false);
    },

    chooseView: function(button, pressed) {
        if (pressed) {
            this.changeView(button.action);
        };
    },

    goToFullscreen: function(tool) {
        this.changeView(portlet.fullscreenTarget);
    },
});
