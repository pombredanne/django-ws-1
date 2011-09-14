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
    ],

    init: function() {
        this.addEvents('new_widget');
        this.control({
            'main': {
                add: this.loadColumns,
            },
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
            portlet = Ext.create('WS.view.layout.Portlet', {
                items: [{
                    xtype: 'taskgrid',
                }],
            });
            component.items.items[0].add(portlet);
            portlet = Ext.create('WS.view.layout.Portlet', {
                html: "kaixo2",
            });
            component.items.items[0].add(portlet);
            portlet = Ext.create('WS.view.layout.Portlet', {
                items: [{
                    xtype: 'processstarter',
                }],
            });
            component.items.items[1].add(portlet);
            portlet = Ext.create('WS.view.layout.Portlet', {
                html: "kaixo3",
            });
            component.items.items[2].add(portlet);
        }
        return true;
    },

    // Add the new widgeth to the dashboard column with less elements
    new_widget: function(view) {
        var dashboard = Ext.ComponentManager.get('dashboard'),
            portlet = Ext.create('WS.view.layout.Portlet', {
                title: view.title_suggestion,
                items: [view],
            }),
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
    }
});
