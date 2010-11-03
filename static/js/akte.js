Ext.onReady(function() {
    // create the data store
    var myDocumentStore = new Ext.data.JsonStore({
            storeId: 'DocumentStore',
            url: 'docs.json',
            restful: true,
            root: 'documents',
            idProperty: 'designator',
            fields: [
                {
                    name: 'datum',
                    type: 'date',
                    dateFormat: 'Y-m-d'
                },
                    'type',
                    'name1',
                    'designator',
                    'quelle',
                    'plz',
                    'ort',
                    'pdf'
                ]
    });

    // load data
    myDocumentStore.load();

MyPanelUi = Ext.extend(Ext.Panel, {
    title: 'Akte',
    width: 720,
    autoHeight: true,
    headerAsText: false,
    unstyled: true,
    collapseFirst: false,
    border: false,
    animCollapse: false,
    initComponent: function() {
        this.items = [
            {
                xtype: 'form',
                title: 'Akte',
                id: 'AkteForm',
                items: [
                    {
                        readOnly: true,
                        xtype: 'textfield',
                        fieldLabel: 'ID',
                        anchor: '100%',
                        itemId: 'designator'
                    },
                    {
                        readOnly: true,
                        xtype: 'textfield',
                        fieldLabel: 'Typ',
                        anchor: '100%',
                        name: 'typ'
                    },
                    {
                        xtype: 'compositefield',
                        fieldLabel: 'Letzte Änderung',
                        name: 'updated',
                        items: [
                            {
                                xtype: 'textfield',
                                flex: 1,
                                name: 'updatet_at',
                                readOnly: true
                            },
                            {
                                xtype: 'textfield',
                                flex: 1,
                                name: 'updated_by',
                                readOnly: true
                            }
                        ]
                    },
                    {
                        xtype: 'compositefield',
                        fieldLabel: 'Angelet',
                        name: 'created',
                        items: [
                            {
                                readOnly: true,
                                xtype: 'textfield',
                                flex: 1,
                                name: 'created_at'
                            },
                            {
                                xtype: 'textfield',
                                flex: 1,
                                name: 'create_by',
                                readOnly: true
                            }
                        ]
                    }
                ]
            },
            {
                xtype: 'grid',
                title: 'Dokumente',
                store: myDocumentStore,
                stripeRows: true,
                frame: true,
                boxMinWidth: 600,
                boxMinHeight: 300,
                autoHeight: true,
                sm: new Ext.grid.RowSelectionModel(
                {
                    singleSelect: true,
                    listeners: {
                        rowselect: function(sm, index, record)
                        {
                            window.location = record.get('pdf');
                        }
                    }
                }),
                columns: [
                    {
                        xtype: 'gridcolumn',
                        header: 'ID',
                        dataIndex: 'designator',
                        sortable: true,
                        width: 100
                    },
                    {
                        xtype: 'datecolumn',
                        header: 'Datum',
                        dataIndex: 'datum',
                        sortable: true
                    },
                    {
                        xtype: 'gridcolumn',
                        header: 'Type',
                        dataIndex: 'type',
                        sortable: true
                    },
                    {
                        xtype: 'gridcolumn',
                        header: 'Name',
                        dataIndex: 'name1',
                        sortable: true,
                        editable: false
                    },
                    {
                        xtype: 'gridcolumn',
                        header: 'PLZ',
                        sortable: true,
                        dataIndex: 'plz'
                    },
                    {
                        xtype: 'gridcolumn',
                        header: 'Ort',
                        sortable: true,
                        width: 100,
                        dataIndex: 'ort'
                    },
                    {
                        xtype: 'gridcolumn',
                        header: 'Dokumentenquelle',
                        dataIndex: 'quelle',
                        sortable: true
                    }
                ]
            },
            {
                xtype: 'form',
                title: 'Kontakt',
                id: 'KontaktForm',
                items: [
                    {
                        readOnly: true,
                        xtype: 'textfield',
                        fieldLabel: 'Name',
                        name: 'name1',
                        anchor: '100%'
                    },
                    {
                        readOnly: true,
                        xtype: 'textfield',
                        fieldLabel: 'Name 2',
                        name: 'name2',
                        anchor: '100%'
                    },
                    {
                        readOnly: true,
                        xtype: 'textfield',
                        fieldLabel: 'Name 3',
                        name: 'name3',
                        anchor: '100%'
                    },
                    {
                        readOnly: true,
                        xtype: 'textfield',
                        fieldLabel: 'Strasse',
                        name: 'strasse',
                        anchor: '100%'
                    },
                    {
                        xtype: 'compositefield',
                        fieldLabel: 'PLZ/Ort',
                        anchor: '100%',
                        items: [
                            {
                                readOnly: true,
                                xtype: 'combo',
                                flex: 1,
                                name: 'land',
                                width: 50
                            },
                            {
                                readOnly: true,
                                xtype: 'textfield',
                                name: 'plz',
                                flex: 1,
                                width: 70
                            },
                            {
                                readOnly: true,
                                xtype: 'textfield',
                                flex: 1,
                                name: 'ort'
                            }
                        ]
                    },
                    {
                        readOnly: true,
                        xtype: 'textfield',
                        fieldLabel: 'E-Mail',
                        name: 'email',
                        anchor: '100%'
                    },
                    {
                        readOnly: true,
                        xtype: 'textfield',
                        fieldLabel: 'Telefon',
                        name: 'telefon',
                        anchor: '100%'
                    },
                    {
                        readOnly: true,
                        xtype: 'textfield',
                        fieldLabel: 'Mobil',
                        name: 'mobil',
                        anchor: '100%'
                    },
                    {
                        readOnly: true,
                        xtype: 'textfield',
                        fieldLabel: 'Fax',
                        name: 'fax',
                        anchor: '100%'
                    }
                ]
            }
        ];
        MyPanelUi.superclass.initComponent.call(this);
    }
});

var panel = new MyPanelUi();
panel.render('aktengrid');
form = Ext.getCmp('AkteForm').getForm().load({ url:'./json', method: 'GET'});
form = Ext.getCmp('KontaktForm').getForm().load({ url:'./json', method: 'GET'});
});
