/**
 * @class Ext.ux.PortalToolbar
 * @extends Ext.Toolbar
 * The main menu of the portal.
 */
Ext.define('Ext.app.PortalToolbar', {
    extend: 'Ext.toolbar.Toolbar',
    alias: 'widget.portaltoolbar',
    //layout: 'fit',
    layout: 'hbox',
    anchor: '100%',
    cls: 'x-portaltoolbar',

    fileMenu: Ext.create('Ext.menu.Menu', {
        items: [{
            text: 'button 1'
        },{
            text: 'button 2'
        }]
    }),

    initComponent: function(){
        Ext.apply(this, {
            items: [{
                text: 'File',
                menu: this.fileMenu
            },{
                text: 'Preferences'
            }]
        });
        this.callParent(arguments);
    }
});
