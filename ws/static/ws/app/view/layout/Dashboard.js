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
                items: [{
                    xtype: 'taskgrid'
                }]
            },{
                html: "kaixo2"
            }],
        },{
            id: "col2",
            items: [{
                items: [{
                    xtype: 'processstarter'
                }]
            }]
        },{
            id: "col3",
            items: [{
                html: "kaixo3"
            }]
        }];

        this.callParent(arguments);

        this.addEvents({
            validatedrop: true,
            beforedragover: true,
            dragover: true,
            beforedrop: true,
            drop: true
        });
        this.on('drop', this.doLayout, this);
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

    initEvents : function(){
        this.callParent();
        this.dd = Ext.create('WS.view.layout.DashboardDropZone', this, this.dropConfig);
    },

    beforeDestroy : function() {
        if (this.dd) {
            this.dd.unreg();
        }
        WS.view.layout.Dashboard.superclass.beforeDestroy.call(this);
    }
});

