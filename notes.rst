--------------------------------------------------------------
[MCP02_01(app_note_BiSS).pdf - AksIM-4 BiSS C Register Access]
--------------------------------------------------------------


#. Naslovi registrov Sensor temperature in C, Signal level in Measured velocity in 0.1 RPM v dokumentaciji niso skladni:

    * stran 6: 0x4E - 0x4F

    * stran 8: 0x4C - 0x4D

    **V novejši verziji dokumenta so naslovi popravljeni**


#. Zakaj niso v podpoglavju *AksIM-4 programming* dodane komande za  E201-9B iz dokumenta *Naloga_testni_inzenir_2.pdf*?


--------------------------------------------------------------
Naloga_testni_inzenir_2.pdf
--------------------------------------------------------------


#. Naloga 1:

    3.c: Piše naj so testi avtomatski, kar je mogoče malo zavajujoče, ker je v **Test branja pozicije** potrebno enkoder zavrteti, torej je test pol-avtomatski?


#. Komande E201-9B

    * Pri opisu komand bi bilo mogoče bolje razdeliti Opis podobno kot v datoteki `E201 USB Encoder Interface <https://www.rls.si/eng/fileuploader/download/download/?d=1&file=custom%2Fupload%2FE201D01_07_bookmark.pdf¨>`_. (Action, interface response with example). Predvsem, da ima vsaka funkcija kratek opis kaj naredi in primer z opisom odgovora

    * V čem se razlikujeta ukaza *X* in *Y*? Ni mi čisto jasno kaj točno naredita...

    * Mogoče bi bilo bolje dodati "Nujno pošljite ta ukaz v primeru, da hočete po prej omenjenih ukazih uporabljati *Control communication* ukaze.", ki se nahaja pri opisu ukaza *Sb* v tabelo *Control Communication*. Sem kar nekaj časa iskal, zakaj ne dobim odgovora pri uporabi ukazov, preden sem pogruntal, da je potrebno resetirati format.