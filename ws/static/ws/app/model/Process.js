Ext.define('WS.model.Process', {
    extend: 'Ext.data.Model',
    fields: ['id', 'title'],

    proxy: {
        type: 'ajax',
        api: {
            read: '/ws/processlaunchers.json',
            update: '/static/ws/data/updateTasks.json'
        },
        reader: {
            type: 'json',
            root: 'processlaunchers',
            successProperty: 'success'
        }
    },

    form_fields: function(callback) {
        Ext.Ajax.request({
            url: '/ws/processlauncher/'+this.data.id+'.json',
            success: function(response) {
                var data = Ext.JSON.decode(response.responseText);
                callback(data['fields']);
            },
        });
    }
});
