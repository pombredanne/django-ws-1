Ext.define('WS.controller.Process', {
    extend: 'Ext.app.Controller',
    stores: ['Processes'],
    models: ['Process'],
    views: [
        'process.Starter',
    ],

    init: function() {
        this.control({
            'processstarter': {
                beforeadd: this.loadProcesses,
            },
            'processstarter button[action=start]': {
                click: this.startProcess
            }
        });
    },

    loadProcesses: function(panel, component) {
        var that = this;
        var store = this.getProcessesStore();
        store.load( function(records, operation, success) {
            if (success) {
                // Add process types as process starter radio fields
                var container = Ext.getCmp('processescontainer');
                console.log("Processes loaded: "+operation.resultSet.count)
                store.each(function(record){
                    this.add({
                        xtype: 'radiofield',
                        boxLabel: record.get('title'),
                        name: 'process',
                        inputValue: record.get('id').toString(),
                        id: 'process_radio'+record.get('id')
                    });
                    return true;
                }, container);
            } else {
                var portlet = panel.up('portlet');
                portlet.setTitle(portlet.title+' (unauthorized)');
                panel.hide();
                var authController = that.getController('Auth');
                authController.fireEvent('auth_required');
            };
        });
    },

    startProcess: function(button) {
        var panel  = button.up('panel'),
            form   = panel.down('form'),
            values = form.getValues(),
            store = this.getProcessesStore(),
            record_idx = store.find('id',values['process']),
            record = store.getAt(record_idx);
            view = Ext.create('WS.view.process.New'),
            layoutController = this.getController('Layout');
        view.update(record.data);
        layoutController.fireEvent('new_widget',view);
    }
});
