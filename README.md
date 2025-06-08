# Šah za četvero igrača
###### Autori: Filip Jerleković i Vito Pokupčić, 3.g
###### Pisano za svrhe projekta za MIOC

Projekt simulira šah za četvero igrača. 
Ploča za igranje je križnog oblika, 14x14 kvadrat bez 3x3 polja u svakom kutu.

## Pokretanje programa
Program se pokreće pokretanjem filea main.py u verziji pythona 3 koja podržava f-stringove.

## Specifična pravila
- Igra se do zadnjeg preostalog igrača
- Igru počinje crveni igrač, nakon čega nastavlja zeleni, pa žuti, pa plavi i tako ukrug
- Iako implicirano, za svaku je stranu orijentacija ploče prilagođena, npr. crveni se pijuni kreću prema gore, zeleni prema lijevo, žuti prema dolje, plavi prema desno
- Promocije se odvijaju na sredini ploče, na istoj relativnoj distanci od početka kao i u standardnom šahu
  - Pijuni se automatski promoviraju u dame kada dođu do zone promocije; tzv. "under-promotion" ne postoji
- Šah te šahmat se provjeravaju na početku poteza igrača
  - Ako zeleni kraljicom šahmatira crvenog te žuti u sljedećem potezu pojede zelenu kraljicu, šahmat je efektivno "poništen" osim ako ga neki drugi igrač ponovno ne zada do kraja kruga.
- Prilikom izvršenog šahmata, sve figure šahmatiranog igrača se brišu s ploče
- Ostala pravila standardnog šaha koja ne kontradiktiraju navedena su (nadam se) uvažena

## Licensa
Prava nemamo, ali ako netko ovaj kod naziva svojim, već je evidentno da ima većih problema u životu uzevši u obzir da je sve u ovom projektu više nego botched te bi svakome s imalo samopoštovanja taj akt trebao biti sramotan. Dakle, tužiti - nećemo.
