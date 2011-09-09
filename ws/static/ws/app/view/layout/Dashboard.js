Ext.define('WS.view.layout.Dashboard', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.dashboard',
    //requires: [
    //    'Ext.layout.component.Body'
    //],

    cls: 'x-dashboard',
    defaultType: 'dashboardcolumn',
    //componentLayout: 'body',
    autoScroll: true,
    layout: 'column',

    initComponent : function() {
        this.items = [{
            id: "col1",
            items: [{
                xtype: 'portlettaskgrid',
            },{
                xtype: 'portlet',
                html: "kaixo2"
            }]
        },{
            id: "col2",
            items: [{
                xtype: 'portlet',
                html: "kaixo3"
            }]
        },{
            id: "col3",
        }];

        this.callParent(arguments);
    },

    // Set columnWidth, and set first and last column classes to allow exact CSS targeting.
    beforeLayout: function() {
        var items = this.layout.getLayoutItems(),
            len = items.length,
            i = 0,
            item;

        for (; i < len; i++) {
            item = items[i];
            item.columnWidth = 1 / len;
            item.removeCls(['x-portal-column-first', 'x-portal-column-last']);
        }
        items[0].addCls('x-portal-column-first');
        items[len - 1].addCls('x-portal-column-last');
        return this.callParent(arguments);
    },

    // private
    //initEvents : function(){
    //    this.callParent();
    //    this.dd = Ext.create('Ext.app.PortalDropZone', this, this.dropConfig);
    //},

    // private
    //beforeDestroy : function() {
    //    if (this.dd) {
    //        this.dd.unreg();
    //    }
    //    Ext.app.PortalPanel.superclass.beforeDestroy.call(this);
    //}
});

