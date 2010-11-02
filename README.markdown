Ablage
======

Ablage ist eine PDF-Archivierungslösung für die AppEngine.

Konzepte
========

Es gibt `Akten`, die Grob einem Geschäftsvorfall (z.B. einer Rechung) Entsprechen. Zu jeder Akte gibt es ein oder mehrere `Dokumente`, die ein Gescanntes PDF beinhalten. Die kann z.B. die eigentliche rechung, eine Mahnung, ein Zahlschein usw sein.

Jedes Dokument hat ein Ausstellungs-`datum` und eine Dokumentennummer (`designator`). Es kann auch eine Adresse nach dem [Simple Address Protocol][1] beinhalten. 



API
===

Akten
-----

    http://d-ablage.appspot.com/uid/akten
    http://d-ablage.appspot.com/uid/akten/{id}


Dokumente
---------

    http://d-ablage.appspot.com/uid/akten/{id}/docs
    http://d-ablage.appspot.com/uid/akten/{id}/docs/{id}


[1]: http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown#readme