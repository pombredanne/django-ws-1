Ext.define('WS.controller.Process', {
    extend: 'Ext.app.Controller',
    stores: [
        'Processes',
        'Workflows',
    ],
    models: [
        'Process',
        'Workflow',
    ],
    views: [
        'process.Starter',
        'process.Portlet',
        'process.Main',
        'process.MainSidebar',
        'process.ProcessDetail',
    ],

    init: function() {
        this.control({
            'processesportlet': {
                beforeadd: this.loadProcesses,
            },
            'processmain gridpanel': {
                selectionchange: this.loadProcessDetail,
            },
        });
    },

    loadProcesses: function(portlet, component) {
        if (component.xtype == 'grid') {
            var that = this;
            this.getProcessesStore().load( function(records, operation, success) {
                if (success) {
                    console.log("Processes loaded: "+operation.resultSet.count)
                } else {
                    portlet.setTitle(portlet.title+' (unauthorized)');
                    var authController = that.getController('Auth');
                    authController.fireEvent('auth_required');
                };
            });
        };
    },

    loadProcessDetail: function(row, selections, options) {
        if (selections.length) {
            var mainpanel = row.view.up('processmain'),
                detailpanel = mainpanel.down('#processdetail'),
                data = selections[0].data,
                detail = Ext.create('WS.view.process.ProcessDetail', data);
            detailpanel.removeAll();
            detailpanel.add(detail);
        }
    }
});
