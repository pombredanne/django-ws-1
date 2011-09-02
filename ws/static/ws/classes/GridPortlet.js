/*

This file is part of Ext JS 4

Copyright (c) 2011 Sencha Inc

Contact:  http://www.sencha.com/contact

GNU General Public License Usage
This file may be used under the terms of the GNU General Public License version 3.0 as published by the Free Software Foundation and appearing in the file LICENSE included in the packaging of this file.  Please review the following information to ensure the GNU General Public License version 3.0 requirements will be met: http://www.gnu.org/copyleft/gpl.html.

If you are unsure which license is appropriate for your use, please contact the sales department at http://www.sencha.com/contact.

*/
Ext.define('Ext.app.GridPortlet', {

    extend: 'Ext.grid.Panel',
    alias: 'widget.gridportlet',
    //height: 300,
    myData: [
        ['1','ordainketa egiaztatu', '/ws/task/1', 'Futurama 1',           'kapitulu berri bat',  '/ws/process/1',           5, '2011/08/31 10:05'],
        ['2','gidoia idatzi',        '/ws/task/1', 'Futurama 1',           'kapitulu berri bat',  '/ws/process/1',           3, '2011/08/31 10:05'],
        ['3','komuna garbitu',       '/ws/task/1', 'lokalaren mantentzea', 'mantentzea',          '/ws/process/1',           1, '2011/08/31 10:05'],
        ['4','argazkiak aukeratu',   '/ws/task/1', '15M erreportaia',      'erreportai grafikoa', '/ws/process/1',           5, '2011/08/31 10:05'],
    ],

    /**
     * Custom function used for column renderer
     * @param {Object} val
     */
    priority: function(val) {
        if (val > 3) {
            return '<span style="background:red;">' + val + '</span>';
        } else if (val < 3) {
            return '<span style="background:green;">' + val + '</span>';
        } else { // val == 3
            return '<span style="background:yellow;">' + val + '</span>';
        }
    },

    /**
     * Custom function used for column renderer
     * @param {Object} val
     */
    link: function(val) {
        return '<a href="'+val+'">'+val+'</a>';
    },

    viewTask: function(grid, rowIndex, colIndex) {
        var record = grid.getStore().getAt(rowIndex);
        var win = Ext.create('Ext.app.Portlet', {
            title: record.get('task'),
            html: 'ID: '+record.get('taskid')+' Process: '+record.get('process'),
        });
        var col = Ext.ComponentManager.get('col-1');
        col.add(win);
        //alert("View " + record.get('taskid')+' '+record.get('task'));
    },

    initComponent: function(){

        var store = Ext.create('Ext.data.ArrayStore', {
            fields: [
               {name: 'taskid'},
               {name: 'task'},
               {name: 'task_link'},
               {name: 'process'},
               {name: 'process_type'},
               {name: 'process_link'},
               {name: 'priority',  type: 'float'},
               {name: 'start_date', type: 'text'}
            ],
            data: this.myData
        });

        Ext.apply(this, {
            //height: 300,
            height: this.height,
            store: store,
            stripeRows: true,
            columnLines: true,
            columns: [{
                id       :'task',
                text   : 'Task',
                //width: 120,
                flex: 1,
                sortable : true,
                xtype : 'templatecolumn',
                tpl: '<a href="{task_link}">{task}</a>'
            },{
                id       :'process',
                text   : 'Process',
                //width: 120,
                flex: 1,
                sortable : true,
                dataIndex: 'process'
            },{
                id       :'process_type',
                text   : 'Process type',
                //width: 120,
                flex: 1,
                sortable : true,
                dataIndex: 'process_type'
            },{
                text   : 'Priority',
                width    : 75,
                sortable : true,
                renderer : this.priority,
                dataIndex: 'priority'
            },{
                text   : 'Date',
                sortable : true,
                dataIndex: 'start_date'
            },{
                xtype:'actioncolumn', 
                //width:50,
                items: [{
                    icon: '/static/ws/images/edit.png',  // Use a URL in the icon config
                    tooltip: 'View',
                    handler: this.viewTask
                }]

            }]
        });

        this.callParent(arguments);
    }
});

