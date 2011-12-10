Ext.define('WS.view.process.Main', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.processmain',
    autoScroll: true,
    title: 'Processes',
    layout: {
        type: 'border',
        padding: 0
    },

    lbar: [{
        xtype: 'fieldset',
        title: 'General actions',
        defaults: {
            xtype: 'button',
        },
        items: [{
            text: 'New',
            action: 'newprocess',
        }],
    },{
        xtype: 'fieldset',
        title: 'Process actions',
        defaults: {
            xtype: 'button',
        },
        items: [{
            text: 'Start',
            action: 'startprocess',
        },{
            text: 'Stop',
            action: 'stopprocess',
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
                store: 'Processes',
                queyModel: 'local',
                typeAhead: 'true',
        }],
    },{
        xtype: 'fieldset',
        title: 'Current Filters',
        html: 'TODO',
    }],

    initComponent: function() {
        this.store = Ext.create('WS.store.Processes', {
            autoLoad: true,
        });
        this.items = [{
            xtype: 'processgrid',
            region: 'center',
            store: this.store,
        },{
            id: 'processdetail',
            region: 'south',
            height: '50%',
            collapsible: true,
            collapseMode: 'mini',
            preventHeader: true,
            split: true,
            items: [{
                title: 'Process details',
                html:'<p>Selecting a process in the grid show\'s detailed information here.</p>',
            }],
        }];
        this.callParent(arguments);
    },
});
