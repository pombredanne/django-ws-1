Ext.define('WS.view.layout.Menubar', {
    extend: 'Ext.toolbar.Toolbar',
    alias: 'widget.menubar',
    layout : 'hbox',

    cls: 'x-menu',

    initComponent : function() {
        // Implement a Container beforeLayout call from the layout to this Container

        this.items = [{
                text: 'File',
                menu: this.fileMenu
            },{
                text: 'Preferences'
            }];

        this.callParent(arguments);
    },

    fileMenu: Ext.create('Ext.menu.Menu', {
        items: [{
            text: 'button 1'
        },{
            text: 'button 2'
        }]
    })


});

