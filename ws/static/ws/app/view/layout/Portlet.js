Ext.define('WS.view.layout.Portlet', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.portlet',
    layout: 'fit',
    anchor: '100%',
    frame: true,
    closable: true,
    collapsible: true,
    animCollapse: true,
    draggable: true,
    resizable: {
        handles: 'n s',
        //pinned: true,
    },
    cls: 'x-portlet',
    refreshable: false,

    initComponent : function() {
        var that = this;
        this.callParent(arguments);
        var tools = [];
        if (this.refreshable == true) {
            tools = tools.concat([{
                type: 'refresh',
                qtip: 'refresh this portlet',
                handler: this.setRefresh,
            }]);
            this.refreshPanel = Ext.create('Ext.toolbar.Toolbar', {
                items: ['->',{
                    xtype: 'label',
                    text: 'Refresh rate (seconds):',
                },{
                    xtype: 'numberfield',
                    name: 'refreshRate',
                    value: 5,
                    minValue: 1,
                    width: 50,
                    listeners: {
                        change: this.updateRefreshInterval,
                    },
                },{
                    xtype: 'checkboxfield',
                    name: 'enableRefresh',
                    checked: false,
                    listeners: {
                        change: this.toggleInterval,
                    },
                },{
                    xtype: 'label',
                    text: 'enabled',
                }],
            });
        };
        if (this.fullscreen == true) {
            tools = tools.concat([{
                type: 'next',
                qtip: 'View in fullscreen',
                action: 'fullscreen',
            }]);
        };
        this.tools = tools;
    },

    setRefresh: function(event, toolEl, panel) {
        var portlet = panel.up('portlet'),
            first = portlet.items.items[0];
        if (first.getXType() == 'toolbar') {
            portlet.remove(portlet.refreshPanel,false); //autodestroy: false
        } else {
            portlet.insert(0, portlet.refreshPanel);
        };
    },

    doRefresh: function(portlet) {
        console.log("Refreshing portlet: "+this.title);
    },

    updateRefreshInterval: function(field, newvalue) {
        var portlet = field.up('portlet'),
            enabled = portlet.down('checkboxfield[name="enableRefresh"]');
        if (enabled.value) {
            if (portlet.refreshInterval) {
                clearInterval(portlet.refreshInterval);
            };
            portlet.refreshInterval = setInterval(function(){
                portlet.doRefresh();
            }, newvalue*1000);
        };
    },

    toggleInterval: function(field, newvalue) {
        console.log("toogle interval:"+newvalue);
        var portlet = field.up('portlet');
        if (portlet.refreshInterval) {
            clearInterval(portlet.refreshInterval);
            portlet.refreshInterval = undefined;
        };
        // newvalue == true => enable refresh
        if (newvalue) {
            var interval = portlet.down('numberfield[name="refreshRate"]');
            console.log("Enable refresh: "+interval.value);
            portlet.refreshInterval = setInterval(function(){
                portlet.doRefresh();
            }, interval.value*1000);
        };
    },

    // Override Panel's default doClose to provide a custom fade out effect
    // when a portlet is removed from the portal
    doClose: function() {
        //remove interval, if any
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
        this.el.animate({
            opacity: 0,
            callback: function(){
                this.fireEvent('close', this);
                this[this.closeAction]();
            },
            scope: this
        });
    },
});
