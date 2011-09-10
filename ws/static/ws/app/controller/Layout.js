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
        this.on('new_widget', this.new_widget);
    },

    // Add the new widgeth to the dashboard column with less elements
    new_widget: function(view) {
        var dashboard = Ext.ComponentManager.get('dashboard'),
            portlet = Ext.create('WS.view.layout.Portlet', {
                items: [view],
            }),
            target_column = -1,
            target_height = 999999,
            column_idx = 0,
            column, column_size;
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
