Ext.define('WS.controller.Process', {
    extend: 'Ext.app.Controller',
    views: [
        'process.Starter',
    ],

    init: function() {
        this.control({
            'processstarter button[action=start]': {
                click: this.startProcess
            }
        });
    },

    startProcess: function(button) {
        console.log('New process started');
    }
});
