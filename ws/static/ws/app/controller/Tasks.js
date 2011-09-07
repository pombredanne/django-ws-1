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

    editTask: function(grid, record) {
        console.log('Double clicked on ' + record.get('name'));
        var view = Ext.widget('taskview');
        view.down('form').loadRecord(record);
    },

    updateTask: function(button) {
        console.log('clicked the Save button');
        var win    = button.up('window'),
            form   = win.down('form'),
            record = form.getRecord(),
            values = form.getValues();

        record.set(values);
        win.close();
        this.getTasksStore().sync();
    }

});
