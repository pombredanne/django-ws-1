Ext.define('WS.controller.Tasks', {
    extend: 'Ext.app.Controller',
    stores: ['Tasks'],
    models: ['Task'],
    views: [
        'task.Portlet',
        'task.Grid',
        'task.View',
    ],

    init: function() {
        this.control({
            'taskportlet': {
                beforeadd: this.loadTasks,
            },
            'taskportlet gridpanel': {
                itemdblclick: this.editTask
            },
            'taskview button[action=save]': {
                click: this.updateTask
            }
        });
    },

    loadTasks: function(grid, component) {
        if (component.xtype == 'grid') {
            var that = this;
            this.getTasksStore().load( function(records, operation, success) {
                if (success) {
                    //console.log("Tasks loaded: "+operation.resultSet.count)
                } else {
                    portlet.setTitle(portlet.title+' (unauthorized)');
                    var authController = that.getController('Auth');
                    authController.fireEvent('auth_required');
                };
            });
        };
    },

    editTask: function(grid, record) {
        //console.log('Double clicked on ' + record.get('task'));
        var view = Ext.widget('taskview');
        view.down('form').loadRecord(record);
        var layoutController = this.getController('Layout');
        layoutController.fireEvent('new_widget',view)
    },

    updateTask: function(button) {
        //console.log('clicked the Save button');
        var panel  = button.up('panel'),
            form   = panel.down('form'),
            record = form.getRecord(),
            values = form.getValues();

        record.set(values);
        win.close();
        this.getTasksStore().sync();
    }

});
