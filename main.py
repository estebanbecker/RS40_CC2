# Réponse 1: Selon cette explication, le critère principale est l'intégrité.
# En effet, selon cette explication, il est très compliqué pour une pirate
# de modifier une transaction sans que cela soit visible par les autres noeuds.
# De plus, si une modification est effectué à un endroit, il faudra modifier
# toutes les transactions suivantes, ce qui est très compliqué.
# En plus, il y a un controle de cohérence des transactions (solde nécessaire, signature de la transaction)
# Réponse 2: Il y a le hash du précédent block. La liste des transactions du block et le hash du block actuel.
# Réponse 3: Il manque dans le block la signature et la preuve de travail.
# Réponse 5: Je peux totalement modifier la somme que me verse l'employeur et ainsi avoir plus d'argent que prévu.
# Réponse 6: Plus il ya  a de 0, plus la preuve de travail est compliqué. Avec six 0, celà fonctionne encore bien, à partir de sept 0
#le temps devient long.


from ecdsa import SigningKey, NIST384p
import hashlib
class Block:
    
    def __init__(self, previous_block_hash, transaction_list, private_key=None):

        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        #Si un clé est annoncé dans le block, on signe la transaction (on admet qu'il n'y a qu'une transaction par block)
        if(private_key == None):
            self.signature = None
        else:
            self.signature = private_key.sign(self.transaction_list[0].encode()).hex()

        #Génération de la preuve de travail, on créé la variabloe poof of work et on l'incrémente jusqu'à ce que le hash du block commence par 0
        self.proof_of_work = -1
        while True:
            self.proof_of_work += 1
            self.block_data = f"{' - '.join(transaction_list)} - {previous_block_hash} - {self.signature} - {self.proof_of_work}"
            self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
            #Modifier ici le nombre de 0 voulu pour la preuve de travail
            if self.block_hash.startswith('000'):
                break
            
            
        

    def check_signature(self, public_key):
        if(self.signature == None):
            return True
        else:
            try:
                #On vérifie la signature avec la clé publique
                public_key.verify(bytes.fromhex(self.signature), self.transaction_list[0].encode())
                return True
            except:
                #Si la signature n'est pas valide, on retourne False
                return False
        
class Blockchain:
    def __init__(self):
        self.chain = []
        self.generate_genesis_block()

    def generate_genesis_block(self):
        self.chain.append(Block("0", ['Genesis Block']))
    
    def create_block_from_transaction(self, transaction_list):
        previous_block_hash = self.last_block.block_hash
        self.chain.append(Block(previous_block_hash, transaction_list))

    #Fonction d'ajout de block avec signature
    def create_block_from_transaction_and_private_key(self, transaction_list, private_key):
        previous_block_hash = self.last_block.block_hash
        self.chain.append(Block(previous_block_hash, transaction_list, private_key))


    def display_chain(self):
        for i in range(len(self.chain)):
            print(f"Data {i + 1}: {self.chain[i].block_data}")
            print(f"Hash {i + 1}: {self.chain[i].block_hash}\n")

    #Fonction de controle de la blockchain pour vérifier l'intégrité
    def check_blockchain(self,public_keys):
        for i in range(len(self.chain)):
            if(self.chain[i].block_hash != hashlib.sha256(self.chain[i].block_data.encode()).hexdigest()):
                return False
            if(i == 0):
                pass
            else:
                #Si le hash n'est pas le même que le hash du block précédent, la blockchain n'est pas valide, elle a été modifié
                if(self.chain[i].previous_block_hash != self.chain[i-1].block_hash):
                    return False
            #On vérifie la signature de chaque block
            if(self.chain[i].check_signature(public_keys[i]) == False):
                return False
        return True

    @property
    def last_block(self):
        return self.chain[-1]


t1 = "L'employeur me verse 2000 €"
t2 = "J'ai dépensé 70 € chez Total"
t3 = "J'ai dépensé 5 € chez amazone"
t4 = "J'ai dépensé 100 € chez Auchan"
t5 = "J'ai dépensé 110 € chez Engi"
t6 = "J'ai dépensé 30 € chez SFR"

#Génération de la clé privée

private_key = SigningKey.generate(curve=NIST384p)
public_key = private_key.get_verifying_key()

myblockchain = Blockchain()
myblockchain.create_block_from_transaction([t1])
print("Block1 created\n")

#On midifie les transactions pour utiliser la signature
myblockchain.create_block_from_transaction_and_private_key([t2], private_key)
print("Block2 created\n")
myblockchain.create_block_from_transaction_and_private_key([t3], private_key)
print("Block3 created\n")
myblockchain.create_block_from_transaction_and_private_key([t4], private_key)
print("Block4 created\n")
myblockchain.create_block_from_transaction_and_private_key([t5], private_key)
print("Block5 created\n")
myblockchain.create_block_from_transaction_and_private_key([t6], private_key)
print("Block6 created\n")

myblockchain.display_chain()


#Verification de la blockchain
public_keys = [public_key, public_key, public_key, public_key, public_key, public_key, public_key]

if(myblockchain.check_blockchain(public_keys)):
    print("La blockchain est valide")
else:
    print("La blockchain n'est pas valide")

#Modifier la valeur pour tester la blockchain face à une modification
#Mis en place pour limiter le temps d'execution quand on utilise le proof of work
if(True):
    #Modification de la blockchain
    myblockchain.chain[2].transaction_list[0] = "J'ai dépensé 500 € chez amazone"

    print("\nModification de la blockchain au milieu\n")

    if(myblockchain.check_blockchain(public_keys)):
        print("La blockchain est valide")
    else:
        print("La blockchain n'est pas valide")

    #Création d'une nouvelle blockchain avec une transaction sans la bonne clé
    myblockchain2 = Blockchain()
    false_private_key = SigningKey.generate(curve=NIST384p)
    myblockchain2.create_block_from_transaction([t1])
    myblockchain2.create_block_from_transaction_and_private_key([t2], private_key)
    myblockchain2.create_block_from_transaction_and_private_key([t3], private_key)
    myblockchain2.create_block_from_transaction_and_private_key([t4], false_private_key)
    myblockchain2.create_block_from_transaction_and_private_key([t5], private_key)
    myblockchain2.create_block_from_transaction_and_private_key([t6], private_key)

    print("\nCréation d'une nouvelle blockchain avec une transaction sans la bonne clé\n")

    if(myblockchain2.check_blockchain(public_keys)):
        print("La blockchain est valide")
    else:
        print("La blockchain n'est pas valide")

