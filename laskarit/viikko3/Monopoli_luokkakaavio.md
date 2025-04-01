## Sovelluslogiikka

Monopolia pelataan käyttäen kahta noppaa. Pelaajia on vähintään 2 ja enintään 8. Peliä pelataan pelilaudalla joita on yksi. Pelilauta sisältää 40 ruutua. Kukin ruutu tietää, mikä on sitä seuraava ruutu pelilaudalla. Kullakin pelaajalla on yksi pelinappula. Pelinappula sijaitsee aina yhdessä ruudussa.

```mermaid
    classDiagram

        class Monopoly{lauta: Pelilauta
        noppa: Tuple[Noppa, Noppa]
        n = in range(2-8)
        pelaajat: Pelaaja*n}

        Monopoly -- Pelilauta
        Pelilauta -- Ruudut
        Monopoly -- Noppa
        Pelilauta -- Pelinappula
        Monopoly -- Pelaaja
        Monopoly -- Pankki

        Monopoly --> Vankila: Monopoly tuntee sijainnin
        Monopoly --> Aloitusruutu: Monopoly tuntee sijainnin


        class Pelilauta{ruudut = [Ruudut]}

        class Ruudut

        class Pankki{id
        raha per pelaaja}

        Vankila --> Ruudut
        Aloitusruutu --> Ruudut
        Sattuma --> Ruudut
        Yhteismaa --> Ruudut
        Normaalit --> Ruudut
        Ruudut --> Ruudut: tuntee viereisten sijainnin



        class Vankila{vieraile()
        jaa()}
        class Aloitusruutu{rahaatulee(200)}
        class Sattuma{sattumakortti}
        class Yhteismaa{yhteismaakortti}
        class Normaalit{nimi: [kadunnimi]
        n: in range(1-4)
        talo: Talo*n
        omistaja: Pelaaja}

        class Noppa{silmäluku: int
        heitto()}

        class Pelaaja{id
        nappula: Pelinappula
        varat: int
        heita()
        siirto()
        maksa()
        }

        class Pelinappula{paikka: Ruudut}
        class Kortti{yhteismaa
        sattuma}
        Yhteismaa ..> Kortti
        Sattuma ..> Kortti

        Talo --> Ruudut
        Hotelli --> Ruudut
        Talo --> Hotelli: Jos 5 taloa yhdessä ruudussa, muuttuu hotelliksi
        class Talo{hinta: int
        sijainti: Ruudut}
        class Hotelli{hinta: int
        sijainti: Ruudut}
```
