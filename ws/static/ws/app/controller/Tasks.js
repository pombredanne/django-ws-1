Ext.define('WS.controller.Tasks', {
    extend: 'Ext.app.Controller',
    stores: ['Tasks'],
    models: ['Task'],
    views: [
        'task.Portlet',
        'task.MyPortlet',
        'task.Grid',
        'task.View',
        'task.TaskDetail',
    ],

    init: function() {
        this.control({
            'tasksmain taskgrid': {
                selectionchange: this.loadTaskDetail,
            },
            'taskdetail form button[action=send]': {
                click: this.sendTaskForm
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
            Ext.Ajax.request({
                url: '/ws/task/'+data['pk']+'/form.json',
                success: function(response) {
                    data['form_fields'] = Ext.JSON.decode(response.responseText);
                    if (!detail) {
                        detail = Ext.create('WS.view.task.TaskDetail', data);
                        var detailpanel = mainpanel.down('#taskdetail');
                        detailpanel.removeAll();
                        detailpanel.add(detail);
                    } else {
                        detail.reloadData(data);
                    }
                }
            });
        }
    },

    sendTaskForm: function(button) {
        var panel = button.up('form'),
            form = panel.getForm(),
            detail = panel.up('taskdetail');
        if (form.isValid()) {
            form.submit({
                url: '/ws/task/'+detail.pk+'/start.json',
                success: function(form, action) {
                    Ext.Msg.alert("task form send");
                },
                failure: function(form, action) {
                    Ext.Msg.alert("error sending task form");
                },
            });
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
