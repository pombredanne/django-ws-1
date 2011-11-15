Ext.define('WS.view.process.PortletNew', {
    extend: 'WS.view.layout.Portlet',
    alias: 'widget.newprocessportlet',
    autoScroll: true,
    title: 'New processes',
    items: [{
        xtype: 'processnewform',
    }],
});
