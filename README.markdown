Ablage
======

Ablage is a PDF archival solution for Google AppEngine.


Konzepte
========

Es gibt `Akten`, die Grob einem Geschäftsvorfall (z.B. einer Rechung) Entsprechen. Zu jeder Akte gibt es ein
oder mehrere `Dokumente`, die ein Gescanntes PDF beinhalten. Die kann z.B. die eigentliche rechung, eine
Mahnung, ein Zahlschein usw sein.

Jedes Dokument hat ein Ausstellungs-`datum` und eine Dokumentennummer (`designator`). Es kann auch eine
Adresse nach dem [Simple Address Protocol][1] beinhalten.


Usage
=====


    git clone http://github.com/mdornseif/Ablage.git
    cd Ablage
    make dependencies
    <edit app.yaml>
    make deploy
    open http://dev.latest.d-ablage.appspot.com/TENANT/akten/

Access control
--------------

You can log in via Google Apps or a uid:secret combination. Set the first uid:secret combination via the Datastore Admin. More can then created via the API.

    curl -X POST -F tenant=TENANT -F admin=True -u $uid:$secret \
        -F text='fuer das Einspeisen von huShop Daten' \
        -F email='edv@example.com' http://localhost:8086/credentials

Every set of credentials is assigned to a tenant which could signify a company or a group of users.
For Google Apps the mapping of domainnames to tenants is currently hardcoded in login.py.


API
===

Objects are usually returned as JSON and contian a `url` Attribute which reference where more about the object can be requested. You have to send and append '.json' to that URL to get the data in an machine readable format. So when you get 

    {
     "url": "http://d-ablage.appspot.com/CYLGI/akten/WL1105302",
     "created_at": "2010-08-24 00:00:00",
     "designator": "WL1105302",
     "updated_at": "2010-11-01 22:15:27.315971",
     "type": "Mahnung",
     "tenant": "CYLGI"
    }

You can request more information at `http://d-ablage.appspot.com/CYLGI/akten/WL1105302.json`. This is to
avoid [browser issues with the accept header][2] and caching issues vith `Vary: Accept` headers.


Search
------
You can search by an objects designator (fast) or do a frefix search on the fields 'designator', 'name1', 'plz', 'email', 'reference', 'name2' and 'ort' (slow). 


    http://d-ablage.appspot.com/uid/search?designator=WL1105302
    http://d-ablage.appspot.com/uid/search?q=4254

Query will return a `results` array which mixes Akte and Document objects. Use the `object` fild to distinguish between them.

    $ curl http://d-ablage.appspot.com/CYLGI/search?q=42549
    {
     "results": [
      {
       "object": "Akte",
       "designator": "WL1188816",
       "url": "http://d-ablage.appspot.com/CYLGI/akten/WL1188816"
       "created_at": "2010-08-26 00:00:00",
       "docs": "http://localhost:8086/CYLGI/akten/WL1188816/docs",
       "email": "k.berger@example.com",
       "land": "DE",
       "name1": "Jane Doe",
       "plz": "42549",
       "strasse": "Uelfestr. 3",
       "tenant": "CYLGI",
       "type": "Rechnung",
       "updated_at": "2010-11-01 22:18:07.654413",
      },
      {
       "object": "Dokument",
       "designator": "F5OQTIGJJNG2IHEFG6EZR3SELA",
       "url": "http://d-ablage.appspot.com/CYLGI/akten/WL1188816/docs/F5OQTIGJJNG2IHEFG6EZR3SELA"
       "akte": "http://d-ablage.appspot.com/CYLGI/akten/WL1188816",
       "created_at": "2010-08-26 00:00:00",
       "datum": "2010-11-01",
       "email": "k.berger@example.com",
       "land": "DE",
       "name1": "Jane Doe",
       "pdf": "http://d-ablage.appspot.com/CYLGI/akten/WL1188816/pdf/F5OQTIGJJNG2IHEFG6EZR3SELA.pdf",
       "plz": "42549",
       "strasse": "Uelfestr. 3",
       "tenant": "CYLGI",
       "type": "Rechnung",
       "updated_at": "2010-11-01 22:18:07.685966",
      }
     ],
     "success": true
    }


Akte
----

Akten (translates as 'File') are the fundamental unit of organisation in the System. You might compare it to a folder. A Akte contains one or more Dokuments (translates as Document). Documents are the equivalent of physical sheets of paper / letters while a Akte logically binds together several documents.

At `http://d-ablage.appspot.com/uid/akten` you can get a list of Akte objects. Single Akte Objects contain some meta-data mainly retrived from the first document in the Akte. The designator should reference the buiseness transaction which resultet in the Akte beeing needed.

    curl http://localhost:8086/CYLGI/akten/WL1188816.json
    {
     "data": {
       "object": "Akte",
       "designator": "WL1188816",
       "url": "http://d-ablage.appspot.com/CYLGI/akten/WL1188816"
       "docs": "http://localhost:8086/CYLGI/akten/WL1188816/docs",
       "created_at": "2010-08-26 00:00:00",
       "email": "k.berger@example.com",
       "land": "DE",
       "name1": "Jane Doe",
       "plz": "42549",
       "strasse": "Uelfestr. 3",
       "tenant": "CYLGI",
       "type": "Rechnung",
       "updated_at": "2010-11-01 22:18:07.654413",
     },
     "success": true
    }

Akte Objects are always implicitly created by creating a document.


Dokument
--------

A Dokument is the fundamental unit of data in Ablage and represents one or more sheets of paper. A Document always references a PDF containing exact that data. A Dokument can be found via the `docs` property of an Akte or via search (see above).

    $ curl http://localhost:8086/CYLGI/akten/WL1188816/docs.json
    {
     "documents": [
      {
       "object": "Dokument",
       "designator": "F5OQTIGJJNG2IHEFG6EZR3SELA",
       "url": "http://d-ablage.appspot.com/CYLGI/akten/WL1188816/docs/F5OQTIGJJNG2IHEFG6EZR3SELA"
       "akte": "http://d-ablage.appspot.com/CYLGI/akten/WL1188816",
       "created_at": "2010-08-26 00:00:00",
       "datum": "2010-11-01",
       "email": "k.berger@example.com",
       "land": "DE",
       "name1": "Jane Doe",
       "pdf": "http://d-ablage.appspot.com/CYLGI/akten/WL1188816/pdf/F5OQTIGJJNG2IHEFG6EZR3SELA.pdf",
       "plz": "42549",
       "strasse": "Uelfestr. 3",
       "tenant": "CYLGI",
       "type": "Rechnung",
       "updated_at": "2010-11-01 22:18:07.685966",
      }
     ],
     "success": true
    }

The data for a single Dokument can be requested at location indicated by the url property, e.g. http://d-ablage.appspot.com/CYLGI/akten/WL1188816/docs/F5OQTIGJJNG2IHEFG6EZR3SELA.json.

Every Document has a `pdf` property where the original document can be retrived.


### Putting Dokument objects in the Ablage

To create a Dokument (and it's associated Akte) POST to `http://d-ablage.appspot.com/CYLGI/docs`. Data should be encoded as `multipart/form-data`. 


#### required fields

* `pdfdata` - raw (scanned) PDF dokument. Currently only document sizes up to 900 kb are supported.
* `ref` - one or more references to order numbers and then like can be given in `ref`. If you want ot give more than one reference, seperate them with spacese (`" "`, `%20`). The first `ref` beeing given will be the `designator` of the Akte. If none is given, the Akte is given an auto-generated id - but you should try to avoid that.
* `type` - the type of Akte / Dokument. E.g. Invoice.


#### optional fields

All fields of the [address protocol][1] (`name1`, `name2`, `name3`, `strasse`, `land`, `plz`, `ort`,
`email`), a reference url (`ref_url`) where human readable information on the document should be available.
The `designator` of a Dokument is always auto-generated and ensures the function is idempotent. The same pdfdata will always return the same document. `datum` should be the date the document was issued/printed or left blank if unknown - it then has to be added by hand later.

The following fields will be filled from their document related counterparts if not given: `akte_name1`,
`akte_name2`, `akte_name3`, `akte_strasse`, `akte_land`, `akte_plz`, `akte_ort`, `akte_email`, `akte_ref_url`, `akte_type`.


 curl -X POST -F pdfdata=@/Users/md/Dropbox/CyberlogiArchiv/DC000167-20100915-1.pdf -F ref=DC000167 -F type=unknown http://localhost:8086/CYLGI/docs



[1]: http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown#readme
[2]: http://www.gethifi.com/blog/browser-rest-http-accept-headers