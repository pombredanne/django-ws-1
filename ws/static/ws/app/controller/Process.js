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
    ],

    init: function() {
        this.control({
            'processesportlet': {
                beforeadd: this.loadProcesses,
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
    }
});
