Ext.define('WS.view.process.NewForm', {
    extend: 'Ext.form.Panel',
    alias: 'widget.processnewform',
    items: [{
        xtype: 'combobox',
        name: 'workflow',
        fieldLabel: 'Workflow',
        valueField: 'pk',
        displayField: 'name',
        store: 'Workflows',
        allowBlank: false,
        typeAhead: true,
    }, {
        xtype: 'checkboxfield',
        fieldLabel: 'Start proccess automatically',
        name: 'autostart',
    }],
    buttons: [{
        text: 'Create',
        action: 'create',
    },{
        text: 'Cancel',
        action: 'cancel',
    }],
});
