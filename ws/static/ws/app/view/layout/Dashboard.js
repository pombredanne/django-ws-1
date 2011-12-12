Ext.define('WS.view.layout.Dashboard', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.dashboard',
    //requires: [
    //    'Ext.layout.component.Body'
    //],

    id: 'dashboard',
    cls: 'x-dashboard',
    defaultType: 'dashboardcolumn',
    //componentLayout: 'body',
    autoScroll: true,
    layout: 'column',

    initComponent : function() {
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

    lbar: [{
        xtype: 'fieldset',
        title: 'Add portlets',
        defaults: {
            xtype: 'button',
        },
        items: [{
            text: 'Tasks',
            action: 'taskPortlet',
        },{
            text: 'My tasks',
            action: 'myTaskPortlet'
        },{
            text: 'Process Starter',
            action: 'startProcess',
        },{
            text: 'Processes',
            action: 'processesPortlet',
        }],
    }],

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
        if (len > 0) {
            items[0].addCls('x-portal-column-first');
        };
        if (len > 1) {
            items[len - 1].addCls('x-portal-column-last');
        };
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

