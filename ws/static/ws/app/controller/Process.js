Ext.define('WS.controller.Process', {
    extend: 'Ext.app.Controller',
    stores: [
        'Processes',
        'RunningProcesses',
    ],
    models: [
        'Process',
        'RunningProcess',
    ],
    views: [
        'process.Starter',
        'process.Running',
    ],

    init: function() {
        this.control({
            'processstarter': {
                beforeadd: this.loadProcesses,
            },
            'processstarter radiofield': {
                change: this.processFields,
            },
            'processstarter button[action=start]': {
                click: this.startProcess
            },
            'runningprocesses': {
                beforeadd: this.loadRunningProcesses,
            },
        });
    },

    loadProcesses: function(panel, component) {
        var that = this;
        var store = this.getProcessesStore();
        store.load( function(records, operation, success) {
            if (success) {
                // Add process types as process starter radio fields
                var container = Ext.getCmp('processescontainer');
                //console.log("Processes loaded: "+operation.resultSet.count)
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

    loadRunningProcesses: function(portlet, component) {
        if (component.xtype == 'grid') {
            var that = this;
            this.getRunningProcessesStore().load( function(records, operation, success) {
                if (success) {
                    //console.log("Running processes loaded: "+operation.resultSet.count)
                } else {
                    portlet.setTitle(portlet.title+' (unauthorized)');
                    var authController = that.getController('Auth');
                    authController.fireEvent('auth_required');
                };
            });
        };
    },

    processFields: function(field, newvalue) {
        if (newvalue == true) {
            var form   = field.up('form'),
                fieldset = form.down('fieldset[title="Process details"]'),
                store = this.getProcessesStore(),
                record_idx = store.find('id',field.inputValue),
                record = store.getAt(record_idx);
            fieldset.removeAll();
            record.form_fields(function(fields) {
                Ext.Array.each(fields, function(field) {
                    fieldset.add([{
                        html: field['help'],
                        cls: 'x-field-help',
                    },{
                        xtype: field['type'], 
                        fieldLabel: field['label'],
                        value: field['default'],
                        name: field['name'],
                    }]);
                });
            });
            fieldset.setVisible(true);
         };
    },

    startProcess: function(button) {
        var panel  = button.up('panel'),
            form   = panel.down('form'),
            values = form.getValues(),
            store = this.getProcessesStore(),
            record_idx = store.find('id',values['process']),
            record = store.getAt(record_idx),
            view = Ext.create('WS.view.process.New'),
            layoutController = this.getController('Layout');
        record.start(values, function(runningprocess) {
            //console.log("Started process id: "+runningprocess.data.id);
        });
        view.update(record.data);
        layoutController.fireEvent('new_widget',view);
    }
});
