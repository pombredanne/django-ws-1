Ext.define('WS.view.layout.Header', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.header',
    height: 70,
    layout : {
        type : 'vbox',
        align: 'stretch'
    },

    cls: 'x-topbar',

    initComponent : function() {
        // Implement a Container beforeLayout call from the layout to this Container

        this.items = [{
               xtype: 'panel',
               height: 40,
               layout: 'hbox',
               items: [
                    Ext.create('Ext.Img', {
                        src: '/static/logo.png',
                    }),
               ]
            },{
                xtype: 'menubar',
            }];

        this.callParent(arguments);
    }

});
