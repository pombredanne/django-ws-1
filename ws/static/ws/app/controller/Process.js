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
        'process.PortletNew',
        'process.Main',
        'process.ProcessDetail',
        'process.NewForm',
    ],

    init: function() {
        this.control({
            'processmain processgrid': {
                selectionchange: this.loadProcessDetail,
            },
            'button[action=newprocess]': {
                click: this.newProcess
            },
            'button[action=startprocess]': {
                click: this.startProcess
            },
            'processnewform button[action=create]': {
                click: this.createProcess
            }
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
    },

    newProcess: function(button) {
        console.log('New process');
        var win = Ext.create('Ext.window.Window', {
                    title: 'New process',
                    closable: true,
                    items: {
                        xtype: 'processnewform',
                    },
                });
        win.show();
    },

    startProcess: function(button) {
        var main = button.up('processmain'),
            grid = main.down('processgrid'),
            sm = grid.getSelectionModel(),
            selection = sm.getSelection();
        Ext.Array.each(selection, function(item) {
            Ext.Ajax.request({
                url: '/ws/process/start.json',
                params: {
                    pk: item.data.pk,
                },
                success: function(response) {
                    data = Ext.JSON.decode(response.responseText)
                    Ext.Msg.alert('Starting process...', data['message']);
                },
            })
        });
    },

    createProcess: function(button) {
        var panel = button.up('form'),
            form = panel.getForm(),
            values = form.getValues(),
            win = panel.up('window');
        if (form.isValid()) {
            console.log("valid form");
            form.submit({
                url: '/ws/process/new.json',
                success: function(form, action) {
                    Ext.Msg.alert("process form send");
                },
                failure: function(form, action) {
                    Ext.Msg.alert("error sending process form");
                },
            });
        }
        //if (win) {
        //    win.close()
        //}
    }
});
