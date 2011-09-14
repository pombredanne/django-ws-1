Ext.define('WS.view.layout.Statusbar', {
    extend: 'Ext.toolbar.Toolbar',
    alias: 'widget.statusbar',
    layout : 'hbox',
    height: 20,

    cls: 'x-status',

    initComponent : function() {
        this.items = [' ', '->','-',{
                xtype: 'tbtext',
                text: 'Status bar',
            }];

        this.callParent(arguments);
    }

});

