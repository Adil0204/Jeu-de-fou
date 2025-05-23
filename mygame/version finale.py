import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

fenetre = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Highway Rush")

# polices
titre_font = pygame.font.SysFont("impact", 48, )
bouton_font = pygame.font.SysFont("impact", 28)
arial24 = pygame.font.SysFont('impact', 24)

# images menu
fond_menu = pygame.image.load("fondmenu.png").convert()
voitures = ["lambo.png", "porsche.png", "fordgt.png", "acura.png"]
voiture_index = 0
voiture_images = []
for voiture in voitures:
    voiture_image = pygame.image.load(voiture).convert_alpha()
    voiture_image = pygame.transform.scale(voiture_image, (50, 100))
    voiture_images.append(voiture_image)

#afficher mon MAGNIFIQUE menu
def afficher_menu():
    fenetre.blit(pygame.transform.scale(fond_menu, (600, 800)), (0, 0))
    titre_surface = titre_font.render("Highway Rush", True, (200, 255, 255))
    fenetre.blit(titre_surface, (160, 130))
    cadre_x, cadre_y, cadre_largeur, cadre_hauteur = 200, 300, 200, 160
    pygame.draw.rect(fenetre, (0, 0, 0), (cadre_x, cadre_y, cadre_largeur, cadre_hauteur))
    pygame.draw.rect(fenetre, (255, 255, 255), (cadre_x + 5, cadre_y + 5, cadre_largeur - 10, cadre_hauteur - 10))
    img = voiture_images[voiture_index]
    img_rect = img.get_rect(center=(cadre_x + cadre_largeur // 2, cadre_y + cadre_hauteur // 2))
    fenetre.blit(img, img_rect)
    touche_surface = bouton_font.render("← / → pour choisir | Entrée pour jouer", True, (0, 0, 0))
    fenetre.blit(touche_surface, (100, 690))
    pygame.display.flip()

def menu():
    global voiture_index
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        afficher_menu()
        for event in pygame.event.get(): #fermez à vos risques et périles (je vous retrouverai)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    voiture_index = (voiture_index - 1) % len(voitures) #pour pouvoir faire défiler les 4 voitures (c'est bas beaucoup mais y'aure des màj) comme un carousel sans devoir revenir en arrière (oui on pense à tout) (index = 0 puis 1 puis 2 puis 3 puis 4 puis reviens à 0)
                elif event.key == pygame.K_RIGHT:                          
                    voiture_index = (voiture_index + 1) % len(voitures) 
                elif event.key == pygame.K_RETURN:
                    return voitures[voiture_index]

voiture_choisie = menu()

#si t'en arrive là c'est que t'es nul et que t'es surement sous substance
def game_over(score, max_score):
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        fenetre.fill((20, 20, 20))
        titre = titre_font.render("GAME OVER", True, (255, 0, 0))
        score_texte = arial24.render(f"Score : {score}", True, (255, 255, 255))
        max_texte = arial24.render(f"Meilleur score : {max_score}", True, (255, 255, 0))
        restart_texte = bouton_font.render("Appuie sur ÉCHAP pour recommencer", True, (255, 255, 255))
        fenetre.blit(titre, (145, 200))
        fenetre.blit(score_texte, (210, 300))
        fenetre.blit(max_texte, (210, 340))
        fenetre.blit(restart_texte, (100, 450))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return #on retourne là où on était avant d'avoir appelé la fonction (c'est pas très clair mais ça marche) et relance notre partie

# joueur et EXPLOSION (non c'est pas du racisme on parle pas des arabes)
imagevoiturejoueur = pygame.image.load(voiture_choisie).convert_alpha()
imagevoiturejoueur = pygame.transform.scale(imagevoiturejoueur, (50, 100))
boum = pygame.image.load("boum.png").convert_alpha()
boum = pygame.transform.scale(boum, (90, 90))

# on charge les ennemis qu'on doit éviter (ou pas si on est kamikaze) parce qu'on est des laches
enemy_files = ["Black_viper.png", "Car.png", "Police.png", "Ambulance.png", "taxi.png", "truck.png", "Mini_truck.png", "Audi.png"]
enemy_images = []
for e in enemy_files:
    enemy_image = pygame.image.load(e).convert_alpha()
    enemy_image = pygame.transform.scale(enemy_image, (100, 110))
    enemy_images.append(enemy_image)


#on importe notre route parce que c'est la base de tout
image_route = pygame.image.load("Toon Road Texture.png").convert_alpha()
image_route = pygame.transform.scale(image_route, (300, 800))
decor_gauche = pygame.image.load("cgauche.png").convert_alpha()
decor_gauche = pygame.transform.scale(decor_gauche, (150, 800))
decor_droit = pygame.image.load("cdroite.png").convert_alpha()
decor_droit = pygame.transform.scale(decor_droit, (150, 800))
#infos sur les positions du joueur
posvoiture = [275, 650]
cible_x = posvoiture[0]

#le son parce que c'est important les EFFETS SPECIAUX DE QUALITE et qu'on aime les bruits de voiture (même si l'électrique c'est plus responsable mais bon, c'est un jeu)
bruit_moteur = pygame.mixer.Sound("moteursss.mp3")
bruit_moteur.set_volume(0.6)
bruit_moteur.play(loops=-1)
musique = pygame.mixer.Sound("GASGASGAS.mp3") #faut pas oublier la musique! (elle est incroyable vous verrez!)
musique.set_volume(0.5)
musique.play(loops = -1)

spawnrate = 1000 #les voitures spawn toutes les secondes au début, cette valeur risque de changer avec les levels (on est des hardcore gamers ici)
ennemis = [] #la liste des ennemis
EVT_SPAWN = pygame.USEREVENT + 1 #événement pour le spawn des ennemis
pygame.time.set_timer(EVT_SPAWN, spawnrate) #on déclenche l'événement toutes les secondes pour l'instant (y'aura peut être des embouteillages)

#un ensemble de variables bien utiles pour mon jeu de fou
enemy_speed = 5
route = pygame.Rect(150, 0, 300, 800)
bordure_gauche = pygame.Rect(130, 0, 20, 800)
bordure_droite = pygame.Rect(450, 0, 20, 800)
speed = 3
offset_route = 0
offset_decor = 0
horloge = pygame.time.Clock()
running = True
tick = 60
seuil_alignement = 2
score = 0
start_ticks = pygame.time.get_ticks()
max_score = 0

#ici on permet au jeu de s'afficher, on gère tout ce qui est le fond et l'affichage des éléments du jeu (pour un max d'éclate)
def dessiner():
    global offset_route, offset_decor
    fenetre.fill((0, 125, 0))
    pygame.draw.rect(fenetre, (255, 255, 0), bordure_gauche)
    pygame.draw.rect(fenetre, (255, 255, 0), bordure_droite)
    # Défilement des décors latéraux (synchronisé avec la route)
    offset_decor = (offset_decor - speed) % decor_gauche.get_height()
    fenetre.blit(decor_gauche, (0, -offset_decor))
    fenetre.blit(decor_gauche, (0, -offset_decor + decor_gauche.get_height()))
    fenetre.blit(decor_droit, (450, -offset_decor))  # 600 - 130
    fenetre.blit(decor_droit, (450, -offset_decor + decor_droit.get_height()))
    offset_route = (offset_route - speed) % image_route.get_height() #Chaque frame, on déplace la route vers le bas (-speed) le modulo (%) permet de revenir à 0 une fois qu’on a défilé toute la hauteur de l’image
    fenetre.blit(image_route, (route.left, -offset_route))
    fenetre.blit(image_route, (route.left, -offset_route + image_route.get_height()))
    score_surface = arial24.render(f"Score : {score}", True, (255,255,255))
    fenetre.blit(score_surface, (20, 20))
    for rect, img in ennemis:
        fenetre.blit(img, (rect.x, rect.y))
    fenetre.blit(imagevoiturejoueur, posvoiture)
    pygame.display.flip()

#gérer la rapidité du jeu selon le score (level augmente --> jeu plus rapide--> un max de fun) WARNING: cela a été réalisé par des professionnels, à ne pas repoduire 
def levelaugmentation(score):
    global enemy_speed, speed, spawnrate
    if score >= 30:
        enemy_speed = 10
        speed = 10
        spawnrate = 1
    if score >= 80:
        enemy_speed = 15
        speed = 15
        spawnrate = 50
    if score >= 110:
        enemy_speed = 17
        speed = 17
        spawnrate = 10
    if score >= 150:
        enemy_speed = 19
        speed = 19
        spawnrate = 10
    return enemy_speed, speed, spawnrate

#ma boucle principale où la magie opère (vroum vroum en avant)
while running:
    horloge.tick(tick)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == EVT_SPAWN: #cette fonction est appelée à chaque fois qu'un ennemi est créé et permet de faire spawn les ennemis sur chaque voie alétoirement (si la chance n'est pas avec vous, il se peut qu'aucune voie sois libre, mais bon, touchons du bois!)
            centres = [200, 300, 400] 
            lane = random.choice([0, 1, 2])     
            x = centres[lane] - 50 
            img = random.choice(enemy_images)
            rect = pygame.Rect(x, -110, 100, 110)
            ennemis.append([rect, img])
        elif event.type == pygame.KEYDOWN: #si on appui sur le clavier eh bah ça BOUGE ! (encore faut-il avoir un clavier avec des flèches)
            if abs(posvoiture[0] - cible_x) < seuil_alignement: # sert à empêcher que le joueur puisse changer de voie tant qu’il n’est pas bien aligné avec une voie avec une marge d'erreur sinon c'est nul
                if event.key == pygame.K_LEFT and cible_x > 150: #on chèque bien que c'est possible d'aller vers la voie cible (faut pas sortir de la route sinon vous allez écraser quelques vaches et deux trois enfants et c'est pas génial)
                    cible_x -= 100 #on change la cible vers la gauche
                elif event.key == pygame.K_RIGHT and cible_x < 340: #de même
                    cible_x += 100 #on change la cible vers la droite

    #on gère le déplacement des ennemis sur l'écran et leur dispartion quand c'est nécessaire
    for ennemi in ennemis:
        ennemi[0][1] += enemy_speed
        if ennemi[0][1] > 800:
            ennemis.remove(ennemi)

    # on check les collisions (faut regarder devant soi quand on conduit sinon ça fait KABOOM!) 
    player_rect = pygame.Rect(posvoiture[0], posvoiture[1], 50, 100)
    for rect, img in ennemis:
        if player_rect.colliderect(rect):
            imagevoiturejoueur = boum
            bruit_moteur.stop()
            musique.stop()
            dessiner()
            pygame.time.delay(1500)
            running = False
            break

    levelaugmentation(score)
    posvoiture[0] += (cible_x - posvoiture[0]) * 0.37 #on permet un déplacement fluide de la voiture entre les voies
    elapsed_ms = pygame.time.get_ticks() - start_ticks
    score = elapsed_ms // 500 #le score est calculé en fonction du temps écoulé depuis le début du jeu (en millisecondes)
    dessiner() #parce que l'art c'est important! (et parce que sinon on voit pas grand chose)

#LOGIQUE DU RESTART:
# Collision détectée ! Le joueur a percuté un ennemi.
# On affiche l'explosion, on stoppe le son moteur, et on met fin à la partie.
# => running = False => la boucle "while running:" se termine.
# Comme tout le code du jeu est à l’intérieur d’une boucle "while True:" générale,
# on passe ensuite à la suite : le score est comparé au record,
# puis l’écran de Game Over est affiché,
# puis on retourne au menu pour rejouer — et tout se réinitialise et c'est reparti

while True:
    if score > max_score:
        max_score = score
    game_over(score, max_score)

    # Réinitialisation des valeurs avant de relancer la partie
    voiture_choisie = menu()
    imagevoiturejoueur = pygame.image.load(voiture_choisie).convert_alpha()
    imagevoiturejoueur = pygame.transform.scale(imagevoiturejoueur, (50, 100))
    posvoiture = [275, 675]
    cible_x = posvoiture[0]
    score = 0
    start_ticks = pygame.time.get_ticks()
    ennemis.clear()
    offset_route = 0
    bruit_moteur.play(loops=-1)
    musique.stop()
    musique.play(loops=-1)
    running = True

    # Et c’est reparti comme en 40
    while running:
        horloge.tick(tick)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == EVT_SPAWN:
                centres = [200, 300, 400]
                lane = random.choice([0, 1, 2])
                x = centres[lane] - 50
                img = random.choice(enemy_images)
                rect = pygame.Rect(x, -110, 100, 110)
                ennemis.append([rect, img])
            elif event.type == pygame.KEYDOWN:
                if abs(posvoiture[0] - cible_x) < seuil_alignement:
                    if event.key == pygame.K_LEFT and cible_x > 150:
                        cible_x -= 100
                    elif event.key == pygame.K_RIGHT and cible_x < 340:
                        cible_x += 100

        for ennemi in ennemis:
            ennemi[0][1] += enemy_speed
        if ennemi[0][1] > 800:
            ennemis.remove(ennemi)

        player_rect = pygame.Rect(posvoiture[0], posvoiture[1], 50, 100)
        for rect, img in ennemis:
            if player_rect.colliderect(rect):
                imagevoiturejoueur = boum
                bruit_moteur.stop()
                musique.stop()
                dessiner()
                pygame.time.delay(1500)
                running = False
                
                break

        levelaugmentation(score)
        posvoiture[0] += (cible_x - posvoiture[0]) * 0.37
        elapsed_ms = pygame.time.get_ticks() - start_ticks
        score = elapsed_ms // 500
        dessiner()
