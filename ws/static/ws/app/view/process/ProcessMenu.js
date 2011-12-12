Ext.define('WS.view.process.ProcessMenu', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.processmenu',
    defaults: {
        xtype: 'button',
    },

    initComponent: function() {
        this.startButton = Ext.create('Ext.Button', {
            text: 'Start',
            action: 'startprocess',
            disabled: true,
        });
        this.stopButton = Ext.create('Ext.Button', {
            text: 'Stop',
            action: 'stopprocess',
            disabled: true,
        });
        this.infoButton = Ext.create('Ext.Button', {
            text: 'Add information',
            action: 'addinfotask',
            disabled: true,
        });
        this.items = [this.startButton, this.stopButton, this.infoButton];
        this.callParent(arguments);
    },

    setButtons: function(status) {
        console.log(status);
        switch(status) {
            case 'PENDING':
                this.startButton.enable();
                this.stopButton.disable();
                this.infoButton.disable();
                break;
            case 'STARTED':
                this.startButton.disable();
                this.stopButton.enable();
                this.infoButton.enable();
            case 'FAILURE':
                this.startButton.disable();
                this.stopButton.disable();
                this.infoButton.enable();
                break;
            default:
        }
    },
});
