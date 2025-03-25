import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

#alussa
    def test_kassapaate_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        
    def test_myydyt_lounaat_edulliset(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_myydyt_lounaat_maukkaat(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

#käteisosto edullinen: 
#onnistuu
    def test_kateinen_ostaessa_edullista_kassa_kasvaa(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
#epäonnistuu
    def test_kateinen_epaonnistuu_edullista_kassa_eikasva(self):
        self.kassapaate.syo_edullisesti_kateisella(50)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
#onnistuu   
    def test_vaihtoraha_edullinen(self):
        onnistuu = self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(onnistuu, 260)
#epäonnistuu
    def test_epaonnistunut_vaihtoraha_edullinen(self):
        koyha = self.kassapaate.syo_edullisesti_kateisella(50)
        self.assertEqual(koyha, 50)
#onnistuu
    def test_kateinen_edullisten_maara_nousee(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.edulliset, 1)
#epäonnistuu    
    def test_kateinen_edullisten_maara_ei_nouse(self):
        self.kassapaate.syo_edullisesti_kateisella(50)
        self.assertEqual(self.kassapaate.edulliset, 0)   



#onnistuu
    def test_kateinen_ostaessa_maukasta_kassa_kasvaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
#epäonnistuu
    def test_kateinen_epaonnistuu_maukasta_kassa_eikasva(self):
        self.kassapaate.syo_maukkaasti_kateisella(50)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
#onnistuu
    def test_vaihtoraha_maukas(self):
        vaihto = self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(vaihto, 100)
#epäonnistuu
    def test_epaonnistunut_vaihtoraha_maukas(self):
        vaihto = self.kassapaate.syo_maukkaasti_kateisella(50)
        self.assertEqual(vaihto, 50)
#onnistuu
    def test_kateinen_maukkaasti_maara_nousee(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.maukkaat, 1)
#epäonnistuu    
    def test_kateinen_maukkaasti_maara_ei_nouse(self):
        self.kassapaate.syo_maukkaasti_kateisella(50)
        self.assertEqual(self.kassapaate.maukkaat, 0)   


#korttiosto edullinen:
#onnistuu
    def test_kortti_ostaessa_edullista_saldo_vähenee(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 760)
#epäonnistuu
    def test_kortti_epäonnistuessa_edullista_saldo_eimuutu(self):
        kortti = Maksukortti(50)
        self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(kortti.saldo, 50)
#onnistuu
    def test_kortti_onnistunut_edullinen(self):
        onnistuu = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(onnistuu, True)
#epäonnistuu
    def test_kortti_epaonnistunut_edullinen(self):
        kortti = Maksukortti(50)
        epaonnistuu = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(epaonnistuu, False)
#onnistuu
    def test_kortti_edullisten_maara_nousee(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)
#epäonnistuu    
    def test_kortti_edullisten_maara_ei_nouse(self):
        kortti = Maksukortti(50)
        epaonnistuu = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(epaonnistuu, 0)   

#korttiosto maukas:
#onnistuu
    def test_kortti_ostaessa_maukasta_saldo_vähenee(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 600)
#epäonnistuu
    def test_kortti_epäonnistuessa_maukasta_saldo_eimuutu(self):
        kortti = Maksukortti(50)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(kortti.saldo, 50)
#onnistuu
    def test_kortti_onnistunut_maukas(self):
        onnistuu = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(onnistuu, True)
#epäonnistuu
    def test_kortti_epaonnistunut_maukas(self):
        kortti = Maksukortti(50)
        epaonnistuu = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(epaonnistuu, False)
#onnistuu
    def test_kortti_maukkaiden_maara_nousee(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)
#epäonnistuu    
    def test_kortti_maukkaiden_maara_ei_nouse(self):
        kortti = Maksukortti(50)
        epaonnistuu = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(epaonnistuu, 0)

#kortin lataus

    def test_kortin_saldo_muuttuu(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 50)
        self.assertEqual(self.maksukortti.saldo, 1050)

    def test_rahaa_ladatessa_kassa_muuttuu(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 50)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100050)

    def test_ei_negatiivista(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -100)
        self.assertEqual(self.maksukortti.saldo, 1000)

#saldo  
    def test_saldo_nakyy_euroina(self):
        euroina = self.kassapaate.kassassa_rahaa_euroina()
        self.assertEqual(self.kassapaate.kassassa_rahaa//100, euroina)

