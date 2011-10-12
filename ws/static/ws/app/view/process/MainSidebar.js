Ext.define('WS.view.process.MainSidebar', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.processsidebar',

    initComponent: function() {
        processStore = Ext.getStore('RunningProcesses');
        this.items = [{
            xtype: 'fieldset',
            title: 'Actions',
            defaults: {
                xtype: 'button',
            },
            items: [{
                text: 'Stop',
                action: 'stopprocess',
            },{
                text: 'Cancel',
                action: 'cancelprocess'
            },{
                text: 'Copy',
                action: 'copyprocess',
            },{
                text: 'Add information',
                action: 'addinfotask',
            }],
        },{
            xtype: 'fieldset',
            title: 'Add Filters',
            items: [{
                xtype: 'combobox',
                fieldLabel: 'Column',
                store: [
                    ['task','Title'],
                    ['user','User'],
                    ['process','Process'],
                    ['process_type','Process type'],
                    ['priority','Priority'],
                    ['date','Date'],
                    ['status','Status'],
                ],
                typeAhead: 'true',
                },{
                    xtype: 'combobox',
                    fieldLabel: 'Value',
                    displayField: 'task',
                    valueField: 'pk',
                    store: processStore,
                    queyModel: 'local',
                    typeAhead: 'true',
            }],
        },{
            xtype: 'fieldset',
            title: 'Current Filters',
            html: 'TODO',
        }];
        this.callParent(arguments);
    },
});

