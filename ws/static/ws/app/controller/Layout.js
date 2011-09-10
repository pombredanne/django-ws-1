Ext.define('WS.controller.Layout', {
    extend: 'Ext.app.Controller',
    views: [
        'layout.Portlet',
        'layout.DashboardColumn',
        'layout.Dashboard',
        'layout.Menubar',
        'layout.Header',
        'layout.Main',
    ],

    init: function() {
        this.addEvents('new_widget');
        this.on('new_widget', this.new_widget);
    },

    // Add the new widgeth to the dashboard column with less elements
    new_widget: function(view) {
        var dashboard = Ext.ComponentManager.get('dashboard'),
            portlet = Ext.create('WS.view.layout.Portlet', {
                items: [view],
            }),
            target_column = -1,
            target_count = 9999,
            column = 0;
        for (column=0; column<dashboard.items.length ; column++) {
            // The second 'items' required, not sure why
            if (target_count > dashboard.items.items[column].items.length) {
                target_column = dashboard.items.items[column];
                target_count = dashboard.items.items[column].items.length;
            }
        }
        target_column.add(portlet);
    }
});
