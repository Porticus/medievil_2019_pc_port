"""Trophies of MediEvil (2019): names, descriptions and grades of the 39 trophies (ids 0..38 as in
sce_sys/trophy/trophy00.trp, matched to its icons), and the files the port keeps them in.

The localized texts inside the .trp are encrypted and are not read: the official texts of the
other languages are in TRANSLATED below, and a language without them shows English."""

import os
from pathlib import Path
import re
import struct

TEXTS = (
    ('Savior of Gallowmere', 'Unlock all trophies.', 'platinum'),
    ('Quest Complete-est', 'Complete all levels in the game.', 'gold'),
    ('Morten Would Be Proud', 'Collect all entries of the Book of Gallowmere.', 'gold'),
    ('King of Cups', 'Collect all the chalice rewards.', 'gold'),
    ('Wolfsbane', 'Defeat the Guardians of the Graveyard.', 'silver'),
    ('A Paneful Demise', 'Defeat the Stained Glass Demon in the Hilltop Mausoleum.', 'silver'),
    ('Demolished the Demons', 'Destroy both Demonettes in the Enchanted Earth.', 'silver'),
    ('Bone Head Bone Dead', 'Defeat the Ghost Ship Captain aboard the Ghost Ship.', 'silver'),
    ('Antagonist', 'Eradicate the Queen Ant and her minions.', 'silver'),
    ('Pulp King Pumpkin', 'Defeat the Pumpkin King in mortal pumpkin combat.', 'silver'),
    ('Not So Scary Now, Eh?', 'Defeat Lord Kardok and his skeletal steed.', 'silver'),
    ('Whack-a-wyrm', 'Defeat the dragon in the Crystal Caves.', 'silver'),
    ('Almost A Hero', 'Give the Knights of Gallowmere everything you have.', 'silver'),
    ('Lost and Found', 'Find all the Lost Souls.', 'silver'),
    ('Soul Savior', 'Lay all the Lost Souls to rest.', 'silver'),
    ('If It Slithers, I Slays', 'Kill the Serpent of Gallowmere.', 'silver'),
    ('Healthiest Man Alive – Er Dead', 'Collect every Life Bottle.', 'silver'),
    ('Sir Moneybags', 'Collect 10,000 gold coins.', 'bronze'),
    ('Old School Sneaky', 'Attempt to perform any original game cheat code.', 'bronze'),
    ('Impaired Drivers', 'Defeat both Mecha Imps and their taunting Imp pilots.', 'bronze'),
    ('Master Dan-At-Arms', 'Collect every weapon.', 'bronze'),
    ('Dizzy Decimator', 'Defeat 30 enemies with the sword spin attack.', 'bronze'),
    ('The Answer Is Chicken', 'Throw 42 chicken legs.', 'bronze'),
    ("Witches' Familiar", 'Collect the Witch Talisman and complete both witch quests.', 'bronze'),
    ('Zip Zap Imp Splat', 'Fry a dozen Imps with Lightning.', 'bronze'),
    ('Gimme That Back!', 'Lose, then recover your weapon from an Imp.', 'bronze'),
    ("It's Not Their Fault They're Mad", "Don't harm the Mad Family.", 'bronze'),
    ('Deathly Smorgasbord', 'Die 7 different ways.', 'bronze'),
    ('Partial To The Potions', 'Drink 32 Health Vials.', 'bronze'),
    ('Now With Added Magic!', 'Enchant the Broad Sword.', 'bronze'),
    ('Mostly Armless', 'Kill something with your own arm.', 'bronze'),
    ('Rock Wrangler', 'Avoid all the rolling rocks on Cemetery Hill.', 'bronze'),
    ("Colonel Fortesque's Special Recipe", 'Turn an enemy into a Roasted Chicken and eat it.', 'bronze'),
    ('Not So Armless', 'Defeat Stained Glass Demon with just your arm.', 'bronze'),
    ('A Shocking Lack Of Respect', 'Destroy 100 gravestones.', 'bronze'),
    ("That's Just Mean!", 'Smash a severed hand.', 'bronze'),
    ('Walls Are For Chumps', "Return to Dan's Crypt and smash down the secret wall.", 'bronze'),
    ('Arsonist', 'Set 50 enemies on fire.', 'bronze'),
    ('Stop Hitting Yourself', 'Get hit by a falling crystal during Dragon battle in Crystal Caves.', 'bronze'),
)
TROPHY_COUNT = len(TEXTS)


# Official PlayStation texts of the other languages, by id as in TEXTS. ru: Stratege; fr: ActuGaming;
# it: TechGaming; es: TrofeosPSN; de: Trophies.de; pt: GameBlast; pl: Variatkowo and Łowcy Trofeów;
# ja: Hima Trophy. No verified source for zh (its PSN text describes an older list), ko, tr or ar: English.
TRANSLATED = {
    'ru': tuple(tuple(row.split(' | ', 1)) for row in '''\
Спаситель Гэллоумира | Получить все призы.
Искатель приключений | Пройти все уровни игры.
Мортен был бы горд | Собрать все записи книги о Гэллоумире.
Король кубков | Собрать все кубки.
Гроза волков | Победить всех кладбищенских стражей.
Осколки смерти | Победить Витражного демона в Мавзолее на холме.
Убийца демонов | Уничтожить обеих демониц в Зачарованной земле.
Просоленные кости | Победить капитана на борту корабля-призрака.
Истребитель муравьев | Избавиться от королевы муравьев и ее слуг.
Пюре из Короля тыкв | Одолеть короля тыкв в смертельном тыквенном бою.
А что-то и не страшно! | Победить лорда Кардока и его костлявого скакуна.
Драконоборец | Победить дракона в Кристальных пещерах.
Почти герой | Отдать рыцарям Гэллоумира все, что у тебя есть.
Потеряшки | Найти все заблудшие души.
Спаситель душ | Упокоить все заблудшие души.
Гроза всех ползючек | Убить Гэллоумирского змея.
Самый здоровый из живых... то есть из мертвых | Собрать все зелья жизни.
Сэр Толстосум | Собрать 10 000 золотых монет.
Хитрец старой закалки | Попытаться использовать любой чит-код из оригинальной игры.
Лихачи | Победить обоих технобесенят и их дерзких пилотов.
Оружейный мастер Дэн | Собрать все оружие.
Головокружительное истребление | Убить 30 врагов круговым ударом меча.
Ответ: курица | Метнуть 42 куриные ножки.
Фамильяр ведьм | Найти ведьминский талисман и выполнить оба ведьминских задания.
Электрибесикация | Поджарить молнией дюжину бесенят.
А ну отдай! | Отбери у бесенка украденное оружие.
Они не виноваты, что крыша поехала | Не причинять вреда безумной семейке.
Смерть на любой вкус | Погибнуть семью разными способами.
Пристрастие к зельям | Выпить 32 эликсира силы.
Теперь и с магией! | Зачаровать широкий меч.
Рукастый | Убить кого-нибудь собственной рукой.
Ловкач | Увернуться от всех катящихся камней на кладбищенском холме.
Особый рецепт полковника Фортескью | Превратить врага в жареную курицу и съесть.
Не такой уж и безрукий | Одолеть Витражного демона одной рукой.
Потрясающее неуважение | Уничтожить 100 надгробных плит.
Это ж подло! | Раздавить отрубленную руку.
Стены — для дураков | Вернуться в склеп Дэна и разбить потайную стену.
Поджигатель | Поджечь 50 врагов.
Аутокристаллизация | Попасть под падающий кристалл во время битвы с драконом в Кристальных пещерах.'''.split('\n')),
    'fr': tuple(tuple(row.split(' | ', 1)) for row in '''\
Sauveur de Gallowmere | Obtiens tous les autres trophées.
Quêtes dûment terminées | Termine tous les niveaux du jeu.
Morten serait fier | Déverrouille toutes les entrées du Grand livre de Gallowmere.
Roi des godets | Récupère toutes les récompenses des Calices.
Tue-loup | Terrasse les Gardiens du Cimetière.
Vitre-aïe | Terrasse le Démon Vitrail au Mausolée de la Colline.
Désenchantées | Détruis les deux démonettes de la Terre Enchantée.
Hisse et os | Bats le Capitaine du vaisseau fantôme à bord de son navire.
1001 baffes | Éradique la Reine des fourmis et ses sbires.
Un peu de courge, jeune homme | Terrasse le Roi Potiron dans un mortel combat de cucurbitacées.
Même pas peur | Terrasse Lord Kardok et son squelette destrier.
Trouble dragon | Terrasse le dragon dans les Cavernes en Cristal.
Quasi-héros | Donne-toi à fond pour les Chevaliers de Gallowmere.
Objets trouvés | Trouve toutes les âmes perdues.
Âme charitable | Offre le repos éternel à toutes les âmes perdues.
Coupé le sifflet | Extermine le Serpent de Gallowmere.
Un mort plein de vie | Récupère tous les flacons de vie.
La bourse ou l’avide | Récupère 10 000 piécettes.
Roublard à l’ancienne | Essaye d’utiliser un code de triche du jeu original.
Le diable au train | Terrasse les Méca-diablotins et leurs conducteurs intrépides.
Daniel, maître ès armes | Obtiens toutes les armes.
Tourbillon trublion | Élimine 30 ennemis avec l’attaque tournoyante de l’épée.
La vie, l’univers et le poulet | Lance 42 cuisses de poulet.
C’est pas sorcier | Récupère le Talisman sorcier et accomplis les deux quêtes des sorcières.
Ça sent le cramé | Fris une douzaine de diablotins avec la foudre.
Rends-moi ça ! | Perds et récupère l’arme des mains du diablotin qui te l’a chipée.
On ne choisit pas d’être fou | Ne fais pas de mal à la famille hypnotisée.
Trépas à toutes les sauces | Meurs de 7 manières différentes.
Sans modération | Bois 32 fioles d’énergie.
Enrichie en magie | Enchante la grande épée.
À bras raccourcis | Élimine un adversaire à la seule force de ton bras.
Roule, ma poule | Évite tous les rochers dévalant la Colline du Cimetière.
Et bon appétit bien sûr | Transforme un ennemi en poulet rôti et mange-le.
À bras-le-corps | Terrasse le Démon Vitrail à la seule force de ton bras.
Manque total de respect | Détruis 100 pierres tombales.
C’est pas gentil ! | Aplatis une main coupée.
Mur de mauviette | Retourne à la Crypte de Daniel et démolis le mur secret.
Pyromane | Mets le feu à 50 ennemis.
Bobo la tête | En affrontant le dragon dans les Cavernes en Cristal, fais-toi heurter par un cristal qui tombe.'''.split('\n')),
    'it': tuple(tuple(row.split(' | ', 1)) for row in '''\
Salvatore di Gallowmere | Sblocca tutti i trofei.
Missione stracompiuta | Completa tutti i livelli del gioco.
Morten sarebbe orgoglioso | Sblocca tutte le voci del Tomo di Gallowmere.
Re di coppe | Ottieni tutte le ricompense dei Calici.
Terrore dei lupi | Sconfiggi i Guardiani del cimitero.
Occhio vitreo | Sconfiggi il Demone della vetrata nel Mausoleo in cima alla collina.
Demonitore | Distruggi entrambe le Diavolette nella Terra Incantata.
Tibie incrociate | Sconfiggi il capitano del Vascello a bordo del Vascello fantasma.
Formicabile | Elimina la regina delle formiche e i suoi sudditi.
Purè di Re Zucca | Sconfiggi il Re Zucca in un combattimento all’ultimo seme.
Ora non fai più così paura, eh? | Sconfiggi Lord Kardok e il suo scheletrico destriero.
Schiacciadrago | Sconfiggi il Drago nelle Caverne di cristallo.
Quasi eroe | Dai tutto ciò che hai ai cavalieri di Gallowmere.
Oggetti smarriti | Trova tutte le anime smarrite.
Guida spirituale | Dona l’eterno riposo a tutte le anime smarrite.
Se striscia è morto | Uccidi il Serpente di Gallowmere.
Salute di ferro (per un morto) | Raccogli tutte le bottiglie della vita.
Sir Taschepiene | Raccogli 10.000 monete d’oro.
Vecchia scuola | Cerca di inserire un trucco qualsiasi del gioco originale.
Guidare con imprudenza | Sconfiggi entrambi i demonietti meccanici e i loro insopportabili piloti.
Dan, maestro d’armi | Ottieni tutte le armi.
Distruttore vorticante | Sconfiggi 30 nemici usando il fendente rotante.
Il pollo è la risposta | Lancia 42 cosce di pollo.
Il famiglio delle streghe | Ottieni il Talismano delle Streghe e completa entrambe le missioni delle streghe.
Demonietti croccanti | Friggi una dozzina di demonietti con la Saetta.
Ridammelo! | Recupera un’arma rubata da un demonietto.
Essere matti non è una colpa | Non ferire la famiglia di matti.
Mille modi per morire… o quasi | Muori in sette modi diversi.
Dipendente dalle pozioni | Bevi 32 fiale d’energia.
Ora con il 50% di magia in più! | Incanta lo spadone.
Braccia rubate all’agricoltura | Uccidi qualcosa usando il tuo braccio.
Caduta massi | Evita tutti i massi rotolanti sulla collina del cimitero.
Ricetta del colonnello Fortesque | Trasforma un nemico in un pollo arrosto e mangialo.
Braccio di ferro | Sconfiggi il Demone della vetrata usando solo il tuo braccio.
Totalmente irrispettoso | Distruggi 100 lapidi.
Volevo solo dare una mano! | Schiaccia una mano mozzata.
I muri non possono fermarmi | Torna alla cripta di sir Dan e distruggi il muro segreto.
Piromane | Dai fuoco a 50 nemici.
Smettila di farti male da solo! | Fatti colpire da un cristallo durante la battaglia con il Drago nelle Caverne di cristallo.'''.split('\n')),
    'es': tuple(tuple(row.split(' | ', 1)) for row in '''\
Salvador de Gallowmere | Desbloquea todos los trofeos.
Misiones completadísimas | Completa todos los niveles del juego.
Morten estaría orgulloso | Recopila todas las entradas del Libro de Gallowmere.
Rey de copas | Reúne todas las recompensas de los cálices.
Matalobos | Derrota a los Guardianes del cementerio.
Un fallecimiento cristalino | Derrota al Demonio de la vidriera en el mausoleo de la Cima de la colina.
Chupaos esa, diablesas | Derrota a las dos diablesas en la Tierra encantada.
Calavera cadavérica | Derrota al fantasma del capitán pirata a bordo del Barco fantasma.
Hormigueo | Erradica a la reina hormiga y a sus esbirros.
Puré de rey Calabaza | Derrota al rey Calabaza en un combate calabacero a muerte.
Ya no das tanto miedo, ¿eh? | Derrota a Lord Kardok y a su montura esquelética.
Machaca al dragón | Derrota al dragón en las Cuevas de cristal.
Casi un héroe | Dalo todo por los caballeros de Gallowmere.
De vuelta al redil | Encuentra todas las almas perdidas.
Salvador de almas | Da descanso a todas las almas perdidas.
Si repta, lo mato | Mata a la serpiente de Gallowmere.
El más sano del cementerio | Reúne todas las botellas de vida.
Sir Pastizal | Reúne 10 000 monedas de oro.
Soplón de la vieja escuela | Intenta utilizar algún truco del juego original.
Pilotos al diablo | Derrota a los dos Robodiablillos y a sus burlones pilotos.
Décimo Dan en armas | Reúne todas las armas.
Diezmador vertiginoso | Derrota a 30 enemigos con el ataque giratorio de la espada.
La respuesta está en el pollo | Tira 42 muslos de pollo.
Familiar de las brujas | Consigue el Talismán de las brujas y completa las misiones de ambas brujas.
Mal rayo te parta, diablillo | Fríe a una docena de diablillos con el rayo.
¡Devuélveme eso! | Pierde tu arma a manos de un diablillo y quítasela otra vez.
No es su culpa que estén locos | No hagas daño a la familia demente.
Una variedad mortal | Muere de 7 maneras distintas.
Debilidad por las pociones | Bebe 32 frascos de energía.
¡Ahora, con magia! | Encanta el espadón.
Mira, mamá, sin brazos | Mata a alguien con tu propio brazo.
Saltarrocas | Evita todas las rocas que caen rodando por la Colina del cementerio.
La receta del coronel Fortesque | Convierte a un enemigo en un pollo asado y cómetelo.
A brazo partido | Derrota al Demonio de la vidriera solo con tu brazo.
Una asombrosa falta de respeto | Destruye 100 lápidas.
¡Tampoco hacía falta eso! | Aplasta una mano cortada.
Las paredes son para lelos | Vuelve a la Cripta de Dan y derriba la pared secreta.
Pirómano | Prende fuego a 50 enemigos.
Deja de pegarte | Déjate golpear por los cristales que caen durante el combate con el dragón en las Cuevas de cristal.'''.split('\n')),
    'de': tuple(tuple(row.split(' | ', 1)) for row in '''\
Gallowmeres Retter | Schalte alle Trophäen frei.
Fix und fertig | Schließe alle Levels des Spiels ab.
Morten wäre stolz | Sammle alle Einträge des Gallowmere-Buchs.
Becherkönig | Sammle alle Kelchbelohnungen.
Wolfsbann | Besiege die Wächter des Friedhofs.
Vorsicht, Glas! | Besiege den Buntglasdämon im Bergmausoleum.
Demolierte Dämoninnen | Vernichte beide Dämoninnen in der Zaubererde.
Toter Totenkopf | Besiege den Geisterschiffkapitän an Bord des Geisterschiffes.
Sturz der Königin | Beseitige die Ameisenkönigin und ihre Untertanen.
Kürbismuskönig | Besiege König Kürbis im Kürbiskampf auf Leben und Tod.
Gar nicht mehr so gruselig, was? | Besiege Lord Kardok und sein Knochenross.
Hau den Lindwurm | Besiege den Drachen in den Kristallhöhlen.
Beinahe ein Held | Gib alles für die Ritter von Gallowmere.
Fundsachen | Finde alle verlorenen Seelen.
Seelenretter | Bette alle verlorenen Seelen zur Ruhe.
Wenn es sich schlängelt, schlage ich zu | Erledige die Schlange von Gallowmere.
Quicklebend- ähm, quicktot? | Sammle alle Lebensflaschen.
Sir Geldsack | Sammle 10.000 Goldmünzen.
Schummler alter Schule | Versuche, einen beliebigen Original-Cheat-Code zu verwenden.
Wie die Wilden | Besiege beide Mecha-Kobolde und ihre höhnischen Koboldpiloten.
Waffenmeister Dan | Sammle alle Waffen.
Schneller Schlitzer | Besiege 30 Gegner mit dem Schwert-Wirbelangriff.
Die Antwort ist Huhn | Wirf 42 Hühnerschlegel.
Hexenvertrauter | Sammle den Hexentalisman und schließe beide Hexenaufträge ab.
Kobold-Kokelei | Röste ein Dutzend Kobolde mit Blitzen.
Gib das zurück! | Verliere deine Waffe an einen Kobold und hol sie dir von ihm zurück.
Sie können nichts dafür, dass sie verrückt sind | Tu der verrückten Familie nichts.
Ungesunde Mischung | Stirb auf 7 verschiedene Arten.
Eine Schwäche für Tränke | Trinke 32 Energiefläschchen.
Jetzt mit Magie! | Verzaubere das Breitschwert.
Arm dran | Erledige einen Gegner mit deinem Arm.
Steinkunstläufer | Weiche allen rollenden Steinen auf dem Friedhofshügel aus.
Oberst Fortesques Spezialrezept | Verwandel einen Gegner in ein Brathähnchen und iss es.
Besser Arm ab als arm dran | Besiege den Buntglasdämon nur mit deinem Arm.
Schockierende Respektlosigkeit | Zerstöre 100 Grabsteine.
Wie gemein! | Zertrümmere eine abgetrennte Hand.
Wände sind für Trottel | Kehre in Dans Krypta zurück und reiße die geheime Wand ein.
Brandstifter | Setze 50 Gegner in Brand.
Hör auf, dich selbst zu schlagen | Lass dich beim Drachenkampf in den Kristallhöhlen von einem fallenden Kristall treffen.'''.split('\n')),
    'pt': tuple(tuple(row.split(' | ', 1)) for row in '''\
Salvador de Gallowmere | Desbloqueie todos os troféus.
Serviço Completo | Termine todos os níveis do jogo.
Orgulho de Morten | Colete todos os registros do Livro de Gallowmere.
Rei de Copas | Colete todos os cálices.
Mata-lobos | Derrote os Guardiões do Cemitério.
Estilhaçou! | Derrote o Demônio do Vitral no Mausoléu da Colina.
Demolidor de Demônios | Destrua os dois Diabinhos na Terra Encantada.
Osso Duro | Derrote o Capitão do Navio Fantasma a bordo do Navio Fantasma.
Tamanduá | Elimine a Formiga Rainha e seus lacaios.
Purê de Abóbora | Derrote o Rei Abóbora em um combate mortal.
Nem Assustou... | Derrote Lorde Kardok e sua montaria esqueleto.
Matador de Dragões | Derrote o dragão nas Cavernas de Cristal.
Quase Um Herói | Dê tudo o que você tiver aos Cavaleiros de Gallowmere.
Achados e Perdidos | Encontre todas as almas perdidas.
Salvador das Almas | Ponha todas as almas perdidas para descansar.
Cobra Criada | Matou a Serpente de Gallowmere.
Um Morto Cheio de Vida | Colete todas as Garrafas de Vida.
Sir Endinheirado | Colete 10.000 moedas de ouro.
Truque das Antigas | Tente usar qualquer código de trapaça do jogo original.
Pilotos Debilitados | Derrote os Diabretes Mecânicos e seus pilotos, diabretes provocadores.
Arsenal Fortesque | Colete todas as armas.
Dizimador Tonto | Derrote 30 inimigos com o ataque de rodopio da espada.
A Resposta É Galinha | Arremesse 42 coxinhas de galinha.
Conhecedor de Bruxas | Colete o Talismã da Bruxa e termine ambas as missões da bruxa.
Churrasquinho de Diabrete | Frite uma dúzia de diabretes com Relâmpago.
Devolva-me Isso! | Perca e depois recupere sua arma de um diabrete.
Não É Culpa Deles | Não machuque a família louca.
Buffet da Morte | Morra de 7 maneiras diferentes.
Uma Queda por Poções | Beba 32 Frascos de Energia.
Agora com Magia! | Encante a Espada Longa.
De Braçada | Mate alguma coisa com o seu próprio braço.
Domador de Pedras | Evite todas as pedras rolando no Cemitério da Colina.
Receita Especial do Coronel Fortesque | Transforme um inimigo em um Frango Assado e coma-o.
Braço de Ferro | Derrote o Demônio do Vitral usando apenas o seu braço.
Falta de Respeito | Destrua 100 lápides.
Isso é cruel! | Esmague uma única mão cortada.
Muros São Inúteis | Retorne até a cripta de Dan e destrua a parede secreta.
Incendiário | Ponha fogo em 50 inimigos.
Não se Machuque! | Seja atingido por um cristal em queda durante a batalha do dragão nas Cavernas de Cristal.'''.split('\n')),
    'pl': tuple(tuple(row.split(' | ', 1)) for row in '''\
Wybawca Gallowmere | Odblokuj wszystkie trofea.
Zadanie najwykonańsze | Ukończ wszystkie poziomy gry.
Morten byłby dumny | Zbierz wszystkie wpisy do Księgi Gallowmere.
Król pucharów | Zbierz wszystkie nagrody za kielichy.
Postrach wilków | Pokonaj strażników cmentarza.
Roztrzaskany | Pokonaj demona z witraża w mauzoleum na wzgórzu.
Demoniczna demolka | Pokonaj obie demonetki na Zaczarowanej Ziemi.
Jolly Roger już śpi | Pokonaj kapitana statku widmo.
Mrówkojad | Pozbądź się królowej mrówek i jej sługusów.
Dżem dyniowy | Pokonaj Dyniowego Króla w śmiertelnym dyniowym boju.
Nie taki Kardok straszny | Pokonaj lorda Kardoka i jego szkieletowego wierzchowca.
Smoking ze smoka | Pokonaj smoka w Kryształowych Jaskiniach.
Prawie jak bohater | Daj z siebie wszystko dla rycerzy Gallowmere.
Biuro rzeczy znalezionych | Znajdź wszystkie zagubione dusze.
Zbawca dusz | Zapewnij wszystkim zagubionym duszom ukojenie.
Ofidiofobia | Zabij Węża z Gallowmere.
Najzdrowszy trup świata | Zbierz wszystkie butelki życia.
Pan Pieniążek | Zbierz 10 000 złotych monet.
Staroszkolny chytrus | Spróbuj wprowadzić dowolny kod oszustwa z pierwszej wersji gry.
Nie za dzielni kierowcy | Pokonaj oba mechaniczne chochliki i ich złośliwych chochliczych pilotów.
Dan zbrojmistrz | Zbierz wszystkie rodzaje broni.
Trąba pomieczna | Pokonaj 30 przeciwników obrotowym ciosem mieczem.
Odpowiedź brzmi – kurczak! | Rzuć 42 udka kurczaka.
Na usługach wiedźm | Zdobądź talizman wiedźmy i ukończ oba wiedźmie zadania.
Smażalnia chochlików | Usmaż tuzin chochlików błyskawicą.
Ej, oddawaj! | Strać, a potem odzyskaj od chochlika swoją broń.
Nie ich wina, że są szaleni | Nie rób krzywdy szalonej rodzinie.
Kolekcjoner zgonów | Zgiń na 7 różnych sposobów.
Trunek na frasunek | Wypij 32 fiolki energii.
Teraz magia w gratisie! | Zaklnij pałasz.
Rękoczyny | Zabij coś swoją własną ręką.
Kamienne rodeo | Uniknij wszystkich toczących się skał na Wzgórzu Cmentarnym.
Wyjątkowy przepis pułkownika Fortesque | Zmień przeciwnika w pieczonego kurczaka, po czym go zjedz.
Rękodzieło | Pokonaj demona z witraża, używając wyłącznie własnej ręki.
Porażający brak szacunku | Zniszcz 100 nagrobków.
To już przesada! | Zniszcz odrąbaną rękę.
Ściany są dla słabych | Wróć do krypty Dana i rozbij tajną ścianę.
Piroman | Podpal 50 przeciwników.
Tego trzeba unikać! | Dostań spadającym kryształem podczas walki ze smokiem w Kryształowych Jaskiniach.'''.split('\n')),
    'ja': tuple(tuple(row.split(' | ', 1)) for row in '''\
ガロメアを救いし者 | 全トロフィーをアンロックする。
クエスト完ぺき主義 | ゲームの全ステージをクリアする。
モーテンが誇りし者 | ガロペディアの全項目を集める。
聖杯の王 | すべての聖杯報酬を集める。
オオカミを倒せし者 | 墓地の守護神を倒す。
砕かれた悪魔 | 教会でステンドグラス・デーモンを倒す。
悪魔払い | 封印の地で２体のデーモネッテをどちらも倒す。
おバカな骨の死 | 海賊船で海賊船のキャプテンを倒す。
アリし日のクイーン | 女王アリとしもべたちを全滅させる。
パルプパンプキング | パンプキン戦においてパンプキングを倒す。
恐れるに足らず？ | カードック卿とガイコツ馬を倒す。
ドラゴンスレイヤー | 水晶の洞窟でドラゴンを倒す。
ほぼほぼヒーロー | ガロメアの騎士たちに持てる力をすべて渡す。
落とし物 | 迷える魂をすべて見つける。
魂の救い手 | 迷える魂をすべて成仏させる。
蛇の道は蛇 | ガロメアの大蛇を退治する。
死してなおヘルシー志向 | ライフボトルをすべて集める。
マネーバッグ卿 | １０,０００枚の金貨を手に入れる。
昔ながらのインチキプレイ | チートコードを入力する。
傷だらけの操縦者たち | ロボットインプと生意気なインプパイロットを倒す。
武器マニア | すべての武器を集める。
切り裂きフォーテスク | 剣のスピンアタックで３０体の敵を倒す。
正解はニワトリ | ４２本のニワトリの足を投げる。
魔女の使い魔 | 魔女の紋章を手に入れて、魔女クエストをどちらもクリアする。
焼き焼きインプ | 稲妻で１２体のインプを倒す。
返しやがれ！ | インプに武器を奪われてその後取り返す。
狂っているのは世界のほうだ | マッド家の人々を傷つけない。
男の死に様 | ７つの異なる方法で死ぬ。
ポーションに首ったけ | ３２個の回復ボトルを飲む。
魔力配合！ | 剣士の剣に魔法をかける。
腕力自慢の腕自慢 | 自分の腕を使って敵を倒す。
大岩スイスイ | 墓地の丘で転がってくる岩をすべて避ける。
フォーテスク大佐のスペシャルレシピ | 敵をローストチキンに変えて食べる。
腕力自慢の腕自慢２ | 自分の腕だけでステンドグラス・デーモンを倒す。
驚くほどのバチ当たり | 墓石を１００個破壊する。
さすがにそりゃひどい！ | うごめく手首を潰す。
壁は勝者のためのもの | 勇者フォーテスクの納骨堂へ戻り、隠し壁を破壊する。
火の用心 | ５０体の敵に火をつける。
頭上注意 | 水晶の洞窟での対ドラゴン戦で、落ちてくる水晶に当たる。'''.split('\n')),
}


def text(trophy, language='en'):
    """(name, description) of a trophy id in a launcher language (English when it has no official
    text); ('', '') for an unknown id."""
    if not 0 <= trophy < TROPHY_COUNT:
        return ('', '')
    return TRANSLATED[language][trophy] if language in TRANSLATED else TEXTS[trophy][:2]


def tier(trophy):
    """'platinum', 'gold', 'silver', 'bronze', or '' for an unknown id."""
    return TEXTS[trophy][2] if 0 <= trophy < TROPHY_COUNT else ''


def write_texts(folder, labels, language):
    """<user dir>/trophy_texts.txt, read by the game at start: the labels of the notice and of the
    in-game list (F8 / R3+R2) and one 'ID=Name | Description' line per trophy. labels: (key, text)
    pairs in the launcher's language. A failure is harmless (the game falls back to English)."""
    lines = [f'# Written by the launcher on every start (language: {language}); do not edit.']
    lines += [f'@{key}={" ".join(value.split())}' for key, value in labels]
    lines += ['{}={} | {}'.format(trophy, *text(trophy, language)) for trophy in range(TROPHY_COUNT)]
    try:
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'trophy_texts.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    except OSError:
        pass


def read_trp_icons(path):
    """{trophy id: PNG bytes} from the game's sce_sys/trophy/trophy00.trp ({} when missing or odd).

    The package header is big endian: magic DC A2 4D 00, file count at 0x10, entry size at 0x14;
    the entries start at 0x60 (32-byte name, offset, size). The icons are TROP000.PNG, TROP001.PNG..."""
    try:
        data = Path(path).read_bytes()
    except OSError:
        return {}
    if len(data) < 0x60 or data[:4] != b'\xdc\xa2\x4d\x00':
        return {}
    count, element = struct.unpack('>II', data[0x10:0x18])
    if not 0x30 <= element <= 0x100:
        return {}
    icons = {}
    for index in range(min(count, 4096)):
        start = 0x60 + index * element
        entry = data[start:start + 0x30]
        if len(entry) < 0x30:
            break
        match = re.fullmatch(r'TROP(\d{3})\.PNG', entry[:0x20].split(b'\0')[0].decode('ascii', 'replace'))
        if not match:
            continue
        offset, size = struct.unpack('>QQ', entry[0x20:0x30])
        if size and offset + size <= len(data):
            icons[int(match.group(1))] = data[offset:offset + size]
    return icons


def read_unlocked(path):
    """The trophy ids the port recorded: <user dir>/trophies.dat holds four little-endian 32-bit words."""
    try:
        raw = Path(path).read_bytes()[:16]
    except OSError:
        return set()
    flags = struct.unpack('<4I', raw.ljust(16, b'\0'))
    return {i for i in range(128) if flags[i // 32] >> (i % 32) & 1}


def reset(path):
    """Locks every trophy again: trophies.dat is moved to trophies.dat.bak (replacing an older copy).
    Returns how many were unlocked (0: nothing changed); OSError when the file cannot be moved.
    The game must be closed: it keeps the trophies in memory while it runs."""
    path = Path(path)
    unlocked = len(read_unlocked(path))
    if unlocked:
        os.replace(path, path.with_name(path.name + '.bak'))
    return unlocked
