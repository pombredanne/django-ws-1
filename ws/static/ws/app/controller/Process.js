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
        'process.Grid',
        'process.Starter',
        'process.Portlet',
        'process.Main',
        'process.MainSidebar',
        'process.ProcessDetail',
    ],

    init: function() {
        this.control({
            'processmain gridpanel': {
                selectionchange: this.loadProcessDetail,
            },
        });
    },

    loadProcessDetail: function(row, selections, options) {
        if (selections.length) {
            var mainpanel = row.view.up('processmain'),
                data = selections[0].data,
                detail = mainpanel.down('processdetail');
            if (!detail) {
                detail = Ext.create('WS.view.process.ProcessDetail', data);
                var detailpanel = mainpanel.down('#processdetail');
                detailpanel.removeAll();
                detailpanel.add(detail);
            } else {
                detail.reloadData(data);
            }
        }
    }
});
