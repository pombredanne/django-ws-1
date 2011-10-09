Ext.define('WS.view.task.MainSidebar', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.tasksidebar',

    initComponent: function() {
        taskStore = Ext.getStore('Tasks');
        this.items = [{
            xtype: 'fieldset',
            title: 'Actions',
            defaults: {
                xtype: 'button',
            },
            items: [{
                text: 'Start',
                action: 'starttask',
            },{
                text: 'End',
                action: 'endtask'
            },{
                text: 'Delegate',
                action: 'delegatetask',
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
                    store: taskStore,
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

