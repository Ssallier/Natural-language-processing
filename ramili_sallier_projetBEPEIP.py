import pandas as pd


train_df = pd.read_csv("./tweets_train.csv", sep=",", header=None, skipinitialspace=True, quotechar='"').values.tolist()
dev_df = pd.read_csv("./tweets_dev.csv", sep=",", header=None, skipinitialspace=True, quotechar='"').values.tolist()
test_df = pd.read_csv("./tweets_test.csv", sep=",", header=None, skipinitialspace=True, quotechar='"').values.tolist()



#Partie 1 
#Lecture du fichier train ; séparation des tweets dans deux listes "pos" et "neg" en fonction du label.
def lecture_train():
    """
    parcourt la liste train_df et sépare les tweets dans 2 listes pos et neg en fonction du label, crée aussi une 3e liste contenant tout les tweets.

    Returns
    -------
    pos : list
        liste des tweets positifs
    neg : list
        liste des tweets négatifs
    tweets_train :
        liste de l'ensemble des tweets

    """
    #création des listes
    pos = []
    neg = []
    liste_glob =[]
    # parcourt de la liste train_df
    for tweets in train_df : 
        # analyse des labels pour determiner la nature du tweet
        if tweets[0]== 'positive':
            pos.append(tweets[1])
            liste_glob.append(tweets[1])
        else : 
            neg.append(tweets[1])
            liste_glob.append(tweets[1])
    # on retourne un tuple contenant les 3 listes
    return (pos,neg,liste_glob)

# création d'une liste contenant l'ensemble des tweets d'entrainement positifs
pos_train = lecture_train()[0]
# création d'une liste contenant l'ensemble des tweets d'entrainement négatifs
neg_train = lecture_train()[1]
#création d'une liste contenant l'ensemble des tweets d'entrainement
tweets_train = lecture_train()[2]

#Lecture des fichiers dev et test : stockages des tweets et labels dans des listes pythons "tweets_dev", "tweets_test", "label_dev" et "label_test".
def lecture_dev_et_test():
    """
    parcourt les listes dev_df et test_df et repartie leurs tweets et leurs labels dans des listes separées (listes tweets_dev et tweets_test pour les tweets
    et label_dev et label_test pour les label).                                                                                                 

    Returns
    -------
    tweets_dev : list
        la liste des tweets de dev.
    tweets_test : list
        la liste des tweets de test.
    label_dev : list
        la liste des labels des tweets de dev
    label_test : TYPE
        la liste des labels des tweets de test

    """
    #creation des listes
    tweets_dev = []
    tweets_test= []
    label_dev = []
    label_test = []
    #parcourt de la liste dev_df
    for tweets in dev_df :
        #ajout de ses tweets à la liste tweets_dev
        label_dev.append(tweets[0])
        #ajout des labels de ses tweets à la liste label_dev
        tweets_dev.append(tweets[1])
    #même opération pour test_df
    for tweets in test_df : 
        label_test.append(tweets[0])
        tweets_test.append(tweets[1])
    #renvoie d'un tuple contenant les 4 listes obtenues
    return (tweets_dev,tweets_test,label_dev,label_test)

# on crée des variables qui contiennent les listes des tweets et des labels 
tweets_dev = lecture_dev_et_test()[0]
tweets_test = lecture_dev_et_test()[1]
label_dev = lecture_dev_et_test()[2]
label_test = lecture_dev_et_test()[3]

def traitement_ponctuation_et_minuscule(t):
    """
    enleve la ponctuation inutile et les majuscules de la str passée en paramètre

    Parameters
    ----------
    t : str
        un tweet sous forme d'une chaine de caractère

    Returns
    -------
    res : str
        le tweet sous la forme d'une chaine de caractère traitée

    """
    #creation d'une nouvelle chaine
    res = ''
    #parcourt les caractères de la chaine passée en parametre, sauf le dernier
    for i in range(len(t)-1):
        #on verifie que le caractère observé et le suivant forment un smiley
        if t[i] in ':;' and t[i+1] in ')(@$D':
            #si c'est le cas, on les ajoutes tous les deux à la nouvelle chaine
            res += t[i] + t[i+1]
        #sinon on verifie que le caractère observé et le suivant forment un coeur
        elif t[i] == '<' and t[i+1] == '3':
            #si c'est le cas, on les ajoute tous les deux à la nouvelle chaine
            res += t[i] + t[i+1]
        #sinon on verifie que le caractère observé et les deux suivants forment un smiley avec un nez
        elif t[i] in ':;' and t[i+1]=='-D' and t[i+2] in ')($@D':
            #si c'est le cas, on les ajoutes tous les trois à la nouvelle chaine
            res += t[i] + t[i+1] + t[i+2]
        #enfin, on verifie que le caractère n'est pas une ponctuation qui fait partie d'un smiley
        elif (t[i] not in '&,-:!?/\#.@;()_"^') and not (t[i] == '3' and t[i-1] == '<') and not(t[i] == 'D' and t[i-1] == ':'):
            #on l'ajoute à la chaine si il ne l'est pas
            res += t[i]
    #on verifie également que le dernier caractère de la chaine n'est pas de la ponctuation inutile
    if t[len(t)-1] not in ';:&,-:!?/\#._"^':
        #et on l'ajoute à la chaine si il ne l'est pas
        res += t[len(t)-1]
    #enfin on retourne la chaine créée tout en minuscule
    return res.lower()

def calcul_occurrence(l):
    """
    crée le dictionnaire d'occurence de l'ensemble des mots d'une liste de chaine de caractère

    Parameters
    ----------
    l : liste
        une liste de chaine de caractère.

    Returns
    -------
    res : dict
        dictionnaire dont les clés sont les mots de la liste passée en parametre, et les valeurs sont les occurences de ces mots dans la liste.

    """
    #création d'une chaine contenant tous les mots presents dans la liste passés en parametres, liste ou on a enlevé la ponctuation inutile et les majuscules
    texte_full = ''
    for tweet in l:
        texte_full += traitement_ponctuation_et_minuscule(tweet) + ' '
    #création d'une liste des mots de ce texte grâce à la fonction .split()
    l_mots = texte_full.split()
    #creation d'un dictionnaire vide
    res = {}
    #on parcourt la liste et on compte les occurences de tous les mots, qu'on repertorie dans le dictionnaire
    for mot in l_mots :
        if mot in res :
            res[mot] += 1
        else:
            res[mot] = 1
    #retour du dictionnaire
    return res
    





def liste_stop_words():
    """
    crée une liste de 30 stop words à partir de la liste des tweets de train 

    Parameters
    ----------
    

    Returns
    -------
    res : list
        la liste des stops words

    """
    #crée le dictionnaire d'occurence de l'ensemble des mots des tweets de tweets_train
    dict_occu = calcul_occurrence(tweets_train)
    liste_occu = []
    res= []
    # on parcourt le dictionnaire
    for mot in dict_occu:
        #on ajoute toutes les valeurs du dictionnaire dans une liste
        liste_occu.append(dict_occu[mot])
    #on trie cette liste dans le sens décroissant 
    liste_occu_trie = sorted(liste_occu, reverse=True)
    #on parcourt la liste des tweets d'entrainements
    for tweet in tweets_train :
        # on traite chaque tweet 
        liste_mots_tweet = traitement_ponctuation_et_minuscule(tweet).split()
        # on parcourt chaque mot du tweet traité
        for mots in liste_mots_tweet :
            # si la valeur de ce mot dans le dictionnaire est dans les 30 premieres valeurs de la liste des valeurs triées ou si la valeur de ce mot est 1 et si le mot n'est pas encore dans la liste des stops words 
            if ((dict_occu[mots] in liste_occu_trie[0:30]) or (dict_occu[mots] == 1)) and (mots not in res):
                # on ajoute ce mot à la liste des stops words
                res.append(mots)
    return res

#on crée une liste qui contiendra les stop words       
les_stop_words = liste_stop_words()

def retire_stop_words(l):
    """
    enleve les stops words des tweets de la liste de tweets passé en paramètre

    Parameters
    ----------
    l : list
    
        une liste de tweets

    Returns
    -------
    res : list
        la liste de tweets sans les stops words

    """
    #création d'une nouvelle liste
    res = []
    #parcourt des tweets de la liste passée en parametre
    for tweet in l:
        #création d'une liste des mots du tweet
        liste_mots_tweet = traitement_ponctuation_et_minuscule(tweet).split()
        #création d'un nouveau tweet, pour l'instant vide
        nouveau_tweet = ' '
        #parcourt des mots de la liste
        for mot in liste_mots_tweet:
            #si le mots n'est pas un stopwords, on l'ajoute au nouveau tweet
            if mot not in les_stop_words :
                nouveau_tweet += mot + ' '
        #ajout du nouveau tweet à la liste finale
        res.append(nouveau_tweet)
    #retour de la liste finale
    return res
    
#on crée les p_pos et p_neg à partir de la liste train car c'est celle qui nous permet de faire les statistiques

p_pos = len(pos_train)/len(tweets_train)
p_neg = len(neg_train)/len(tweets_train)

#on crée une liste des tweets d'entrainement sans les stop words
tweets_train_traites = retire_stop_words(tweets_train)


def nombre_liste_mots(l):
    """
    
renvoie la liste de tout les mots différents ainsi que le nombre de mots d'une liste de tweets déjà traitées
    Parameters
    ----------
    l : list
        une liste de tweets deja traitée

    Returns
    -------
    type : tuple
        un tuple contenant le nombre de mots d'un tweet ainsi que la liste de tous les mots différents

    """
    nb = 0
    liste = []
    # on parcourt chaque tweets de la liste
    for tweets in l :
        # on parcourt chaque mots du tweet
        for mots in tweets.split() :
            # on incrémente le compteur de mots
            nb += 1
            # si le mot n'est pas dans la liste des mots différents
            if mots not in liste:
                #on ajoute le mot dans cette liste
                liste.append(mots)
    return (nb,liste)
    
# création d'une variable qui contient le nombre de mots dans la liste des tweets d'entrainement traités
n_corp = nombre_liste_mots(tweets_train_traites)[0]
# création d'une liste qui contient tous les mots différents de la liste des tweets d'entrainement 
mots_corp = nombre_liste_mots(tweets_train_traites)[1]

def liste_mots_total(l):
    """
    

    Parameters
    ----------
    l : list
        une liste de tweets deja traitée.

    Returns
    -------
    res : list
        une liste contenant tous les mots presents dans la liste de twets.

"""
    #creation d'une liste vide
    res = []
    #ajout des mots de chaque tweets un par un dans la nouvelle liste
    for tweets in l:
        for mots in tweets.split():
            res.append(mots)
    #retour de la liste
    return res
  
# création d'une liste qui contient l'ensemble des mots de tweet train
liste_mots_train_traites = liste_mots_total(tweets_train_traites)
#création d'une liste qui contient l'ensemble des mots des tweets d'entrainements positifs 
liste_mots_pos_traites = liste_mots_total(retire_stop_words(pos_train))
#création d'une liste qui contient l'ensemble des mots des tweets d'entrainements négatifs 
liste_mots_neg_traites = liste_mots_total(retire_stop_words(neg_train))


def occurence_mots_tweets(liste_mot_diff,liste_mots_tot):
    """
    

    Parameters
    ----------
    liste_mot_diff : list
        la liste des mots différents d'une liste de tweets traités
    liste_mots_tot : list
        la liste des tout les mots d'une liste de tweets traités

    Returns
    -------
    res : list
        une liste d'entiers ou chaque entier à l'indice i correspond au nombre de fois ou le mots d'indice i dans la liste des mots différents apparait dans la liste totale des mots

    """
    #création d'une liste de longueur égale au nombre de mots différents
    res = [0]*len(liste_mot_diff)
    # on crée une boucle de longueur égale à la liste précédente qui va nous permettre d'incrémenter la valeur des indices
    for i in range(len(liste_mot_diff)):
        # on parcourt la liste de tout les mots
        for mots in liste_mots_tot:
            # on incrémente l'indice de la liste résultat si on trouve le mot dans la liste de tout les mots
            if liste_mot_diff[i] == mots:
                res[i] += 1
    return res
    
# création de la liste d'occurence des mots des tweets d'entrainement
occur_corp = occurence_mots_tweets(mots_corp,liste_mots_train_traites)
#variable contenant le nombre de mots positifs des tweets d'entrainement
n_pos = nombre_liste_mots(retire_stop_words(pos_train))[0]
# création de la liste de tout les mots positifs différents des tweets d'entrainement.
mots_pos = nombre_liste_mots(retire_stop_words(pos_train))[1]
# variable contenant le nombre de mots négatifs des tweets d'entrainement
n_neg = nombre_liste_mots(retire_stop_words(neg_train))[0]
# création de la liste de tout les mots négatifs différents des tweets d'entrainement
mots_neg = nombre_liste_mots(retire_stop_words(neg_train))[1]
#création de la liste d'occurence des mots positifs des tweets d'entrainement
occur_pos = occurence_mots_tweets(mots_pos, liste_mots_pos_traites)
#création de la liste d'occurence des mots négatifs des tweets d'entrainement
occur_neg = occurence_mots_tweets(mots_neg, liste_mots_neg_traites)

def proba_mot(mot):
    """
    calcul de la probabalité d'un mot passé en paramettre

    Parameters
    ----------
    mot : str
        le mot dont on souhaite determiner la probabilité

    Returns
    -------
    res : float
        la probabilité du mot passé en paramettre

    """
    indice_mot = -1
    #recherche de la position du mot dans la liste mot_corp
    for i in range (len(mots_corp)):
        if mots_corp[i] == mot :
            indice_mot = i
    #si le mot est present dans mot_corp on retourne l'occurence de se mot dans le corpus divisé par le nombre de mots total
    if indice_mot != -1:
        res = occur_corp[indice_mot]/n_corp
    #sinon, on retourne 0
    else :
        res = 0
    return res

def proba_mot_sachant_pos(mot): 
    """
    

    Parameters
    ----------
    mot : str
        un mot

    Returns
    -------
    res : float
        la probabilité que le mot soit positif sachant que le tweet est positif

    """
    indice_mot = -1
    # on crée une boucle de longueur égale à l'ensemble des mots positifs différents (liste mots_pos)
    for i in range (len(mots_pos)):
        # si on trouve le mot passé en parametre dans la liste des mots positifs différents
        if mots_pos[i] == mot :
            #on stocke l'indice du mot passé en parametre
            indice_mot = i
    #si on a trouvé le mot passé en parametre dans la liste des mots positifs
    if indice_mot != -1:
        # on calcule la probabilité de ce mot (nombre d'occurence du mot divisé par le nombre de mots positifs)
        res = occur_pos[indice_mot]/n_pos
    # si on n'a pas trouvé le mot dans la liste des mots positifs
    else :
        res = 0
    # on retourne la probabilité du mot
    return res

def proba_mot_sachant_neg(mot): 
    """
    

    Parameters
    ----------
    mot : str
        un mot

    Returns
    -------
    res : float
        la probabilité que le mot soit negatif sachant que le tweet est negatif

    """
    indice_mot = -1
    # on crée une boucle de longueur égale à l'ensemble des mots negatifs différents (liste mots_neg)
    for i in range (len(mots_neg)):
        # si on trouve le mot passé en parametre dans la liste des mots negatifs différents
        if mots_neg[i] == mot :
            #on stocke l'indice du mot passé en parametre
            indice_mot = i
    #si on a trouvé le mot passé en parametre dans la liste des mots negatifs
    if indice_mot != -1:
        # on calcule la probabilité de ce mot (nombre d'occurence du mot divisé par le nombre de mots negatifs)
        res = occur_neg[indice_mot]/n_neg
    # si on n'a pas trouvé le mot dans la liste des mots negatifs
    else :
        res = 0
    #on retourne la probabilité du mot
    return res
    
tweet_dev_traites = retire_stop_words(tweets_dev)
            
def proba_label_sachant_tweet(tweet):
    """
    

    Parameters
    ----------
    tweet : str
        un tweet traité 

    Returns
    -------
    label : str
    'positive' si la proba que le tweet est positif est supérieure à la proba que le tweet soit négatif
    'negative' si la proba que le tweet est negatif est supérieure à la proba que le tweet soit positif
    

    """
    label =''
    proba_tweet_sachant_pos = 1
    proba_tweet_sachant_neg = 1
    proba_tweet_p = 1
    proba_tweet_n = 1
    liste_mots_pos = []
    liste_mots_neg = []
    
    #Remplissage des liste liste_mots_pos et liste_mots_neg 
    for mots in tweet.split() :
        if mots in mots_pos :
            liste_mots_pos.append(mots)
        if mots in mots_neg :
            liste_mots_neg.append(mots)
   
    #Calcule des proba_tweet_sachant_pos et proba_tweet_p 
    for mot in liste_mots_pos:
        proba_tweet_sachant_pos *= proba_mot_sachant_pos(mot)
        proba_tweet_p *= proba_mot(mot)
    
    #Calcule des proba_tweet_sachant_neg et proba_tweet_n
    for mot in liste_mots_neg:
        proba_tweet_sachant_neg *= proba_mot_sachant_neg(mot)
        proba_tweet_n *= proba_mot(mot)
    
    #Calcule des proba_pos_sachant_tweet et proba_neg_sachant_tweet  
    proba_pos_sachant_tweet = (p_pos*proba_tweet_sachant_pos)/proba_tweet_p
    proba_neg_sachant_tweet = (p_neg*proba_tweet_sachant_neg)/proba_tweet_n
    if proba_pos_sachant_tweet > proba_neg_sachant_tweet :
        label = 'positive'
    else :
        label = 'negative'
    return label 
    

def labelisation_liste_tweet(l):
    """
    renvoie la liste des prédictions des labels d'une liste passée en paramètre (non traitée)'

    Parameters
    ----------
    l : list
        une liste de tweets à labeler.

    Returns
    -------
    res : list
        la liste des probabilités que chaque tweet soit positif ou negatifs.
    """
    #supression des stops words de la liste de tweet
    liste_tweet_traite = retire_stop_words(l)
    #creation d'une nouvelle liste
    res = []
    for tweets in liste_tweet_traite :
        #ajout du label prédit par les probabilités pour chaque tweet dans la nouvelle liste
        res.append(proba_label_sachant_tweet(tweets))
    #retour de la nouvelle liste
    return res 

def compare_label(l1,l2):
    """
    

    Parameters
    ----------
    l1 : list
        la liste des labels prédits à partir des fonctions précédentes
    l2 : list
        une liste de labels, liste "référence"

    Returns
    -------
    float
        le pourcentage de label prédits qui correspondent aux labels de la liste de référence 

    """
    cpt = 0 
    # on crée une boucle qui va nous permettre de parcourir les 2 listes en simultané 
    for i in range(len(l1)):
        # si le label prédit est le même que le label de référence
        if l1[i]==l2[i]:
            # on incrémente un compteur 
            cpt+=1
    # on retourne le nombre de label correctement prédit divisé par le nombre total de label multiplié par 100 pour obtenir un pourcentage.
    return (cpt/len(l1))*100



print(compare_label(labelisation_liste_tweet(tweets_dev),label_dev))
print(compare_label(labelisation_liste_tweet(tweets_test),label_test))
