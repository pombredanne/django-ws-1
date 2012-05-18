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
        'process.ProcessMenu',
    ],

    init: function() {
        this.control({
            'processmain processgrid': {
                selectionchange: this.updateProcessView,
            },
            'button[action=newprocess]': {
                click: this.newProcess
            },
            'button[action=startprocess]': {
                click: this.startProcess
            },
            'button[action=stopprocess]': {
                click: this.stopProcess
            },
            'processnewform button[action=create]': {
                click: this.createProcess
            }
        });
    },

    updateProcessView: function(row, selections, options) {
        if (selections.length) {
            var mainpanel = row.view.up('processmain'),
                data = selections[0].data,
                menu = mainpanel.down('processmenu');
            menu.setButtons(data['status']);
            this.loadProcessDetail(mainpanel, data);
        }
    },

    loadProcessDetail: function(mainpanel, data) {
        var detail = mainpanel.down('processdetail');
        if (!detail) {
            detail = Ext.create('WS.view.process.ProcessDetail', data);
            var detailpanel = mainpanel.down('#processdetail');
            detailpanel.removeAll();
            detailpanel.add(detail);
        } else {
            detail.reloadData(data);
        }
    },

    newProcess: function(button) {
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

    stopProcess: function(button) {
        var main = button.up('processmain'),
            grid = main.down('processgrid'),
            sm = grid.getSelectionModel(),
            selection = sm.getSelection();
        Ext.Array.each(selection, function(item) {
            Ext.Ajax.request({
                url: '/ws/process/stop.json',
                params: {
                    pk: item.data.pk,
                },
                success: function(response) {
                    data = Ext.JSON.decode(response.responseText)
                    Ext.Msg.alert('Stoppint process...', data['message']);
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
            form.submit({
                url: '/ws/process/new.json',
                success: function(form, action) {
                    Ext.Msg.alert("Success", action.result.message);
                    win.close();
                },
                failure: function(form, action) {
                    Ext.Msg.alert("Error", action.result.message);
                },
            });
        }
    }
});
