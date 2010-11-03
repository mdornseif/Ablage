Ext.onReady(function() {

    // create the data store
    var store = new Ext.data.JsonStore({
        xtype: 'jsonstore',
        storeId: 'MyStore',
        url: 'http://localhost:8086/CYLGI/akten.json',
        root: 'akten',
        autoLoad: true,
        restful: true,
        fields: [
        {
            name: 'designator',
            allowBlank: false
        },
        {
            name: 'created_at',
            type: 'date',
            dateFormat: 'Y-m-d'
        },
        'tenant', 'name1', 'url'
        ]
    });

    // load data
    store.load();

    // create the Grid
    var grid = new Ext.grid.GridPanel({
        store: store,
        columns: [
        {
            id: 'designator',
            header: "ID",
            sortable: true,
            dataIndex: 'designator'
        },
        {
            header: 'Name',
            sortable: true,
            dataIndex: 'name1'
        },
        {
            header: 'Ab',
            xtype: 'datecolumn',
            sortable: true,
            dataIndex: 'created_at'
        },
        {
            header: 'tenant',
            sortable: true,
            dataIndex: 'tenant'
        }
        ],
        stripeRows: true,
        height: 250,
        width: 500,
        title: 'Akten',
        sm: new Ext.grid.RowSelectionModel(
        {
            singleSelect: true,
            listeners: {
                rowselect: function(sm, index, record)
                {
                    window.location = record.get('url') + '/';
                }
            }
        }),
        bbar: new Ext.PagingToolbar({
            pageSize: 25,
            store: store,
            displayInfo: true,
            displayMsg: 'Displaying topics {0} - {1} of {2}',
            emptyMsg: "No topics to display"
        })

    });
    grid.render('aktengrid');
});