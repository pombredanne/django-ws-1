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
        if (this.refreshable == true) {
            this.tools = [{
                type: 'refresh',
                qtip: 'refresh this portlet',
                handler: this.setRefresh,
            }];
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
                    checked: true,
                    listeners: {
                        change: this.toggleInterval,
                    },
                },{
                    xtype: 'label',
                    text: 'enabled',
                }],
                hidden: true,
            });
            this.insert(0,this.refreshPanel);
            this.refreshInterval = setInterval(function(){
                    that.doRefresh()
            }, 5000);
        }
    },

    setRefresh: function(event, toolEl, panel) {
        var portlet = panel.up('portlet');
        if (portlet.refreshPanel.isHidden()) {
            portlet.refreshPanel.show()
        } else {
            portlet.refreshPanel.hide()
        }
        portlet.doRefresh();
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
