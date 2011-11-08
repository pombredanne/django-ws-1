Ext.define('WS.view.process.ProcessDetail', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.processdetail',
    autoScroll: true,
    height: 500,
    layout: {
        type: 'border',
        padding: '0 5 5 5'
    },

    initComponent: function() {
        this.title = 'Process title';
        this.items = [{
            region: 'east',
            items: [{
                html: 'Process graph',
            }],
        },{
            region: 'center',
            items: [{
                html: 'Process details',
            }],
        }];
        this.callParent(arguments);
    },
});

