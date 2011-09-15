Ext.define('WS.model.Process', {
    extend: 'Ext.data.Model',
    fields: ['id', 'title'],

    form_fields: function() {
        var fields = [{
            'label': 'Title',
            'type': 'textfield',
            'default': '',
            'help': 'The title of this process.'
        },{
            'label': 'Description',
            'type': 'textfield',
            'default': 'This is the description',
            'help': 'The description of this process.'
        }];
        console.log("Process id"+this.data.id);
        if (this.data.id == 1) {
            fields.push({
            'label': 'Date',
            'type': 'datefield',
            'default': 'jajaj',
            'help': 'jojo.'
            });

        }
        return fields
    }
});
