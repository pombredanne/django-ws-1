Ext.define('WS.controller.Tasks', {
    extend: 'Ext.app.Controller',
    stores: ['Tasks'],
    models: ['Task'],
    views: [
        'task.Grid',
        'task.View',
    ],

    init: function() {
        //console.log('Initialized Tasks! This happens before the Application launch function is called');
        this.control({
            //'viewport > panel': {
            //    render: this.onPanelRendered
            //},
            'taskgrid': {
                beforeadd: this.loadTasks,
                itemdblclick: this.editTask
            },
            'taskview button[action=save]': {
                click: this.updateTask
            }
        });
    },

    //onPanelRendered: function() {
    //    console.log('The panel was rendered');
    //},
    
    loadTasks: function(grid, component) {
        var that = this;
        this.getTasksStore().load( function(records, operation, success) {
            if (success) {
                console.log("Tasks loaded: "+operation.resultSet.count)
            } else {
                var portlet = grid.up('portlet');
                portlet.setTitle(portlet.title+' (unauthorized)');
                grid.hide();
                var authController = that.getController('Auth');
                authController.fireEvent('auth_required');
            };
        });
    },

    editTask: function(grid, record) {
        console.log('Double clicked on ' + record.get('task'));
        var view = Ext.widget('taskview');
        view.down('form').loadRecord(record);
        var layoutController = this.getController('Layout');
        layoutController.fireEvent('new_widget',view)
    },

    updateTask: function(button) {
        console.log('clicked the Save button');
        var panel  = button.up('panel'),
            form   = panel.down('form'),
            record = form.getRecord(),
            values = form.getValues();

        record.set(values);
        win.close();
        this.getTasksStore().sync();
    }

});
