Ext.define('WS.controller.Tasks', {
    extend: 'Ext.app.Controller',
    stores: ['Tasks'],
    models: ['Task'],
    views: [
        'task.Portlet',
        'task.Grid',
        'task.View',
        'task.TaskDetail',
    ],

    init: function() {
        this.control({
            'tasksmain taskgrid': {
                selectionchange: this.loadTaskDetail,
            },
            'taskportlet gridpanel': {
                itemdblclick: this.editTask
            },
            'taskview button[action=save]': {
                click: this.updateTask
            }
        });
    },

    loadTaskDetail: function(row, selections, options) {
        if (selections.length) {
            var mainpanel = row.view.up('tasksmain'),
                data = selections[0].data,
                detail = mainpanel.down('taskdetail');
            if (!detail) {
                detail = Ext.create('WS.view.task.TaskDetail', data);
                var detailpanel = mainpanel.down('#taskdetail');
                detailpanel.removeAll();
                detailpanel.add(detail);
            } else {
                detail.reloadData(data);
            }
        }
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
