# Simulatore di tempeste
I Guardatempeste hanno bisogno di un software python per simularne il comportamento.

I moduli e le classi vanno sviluppati nel package *tempest*.
Non spostare o rinominare moduli e classi esistenti e non modificare le signature dei metodi.

In *main.py* viene fornito del semplice codice, da voi modificabile, che testa le funzionalità base.
Esso mostra esempi di uso dei metodi principali ed esempi dei controlli richiesti.

Tutte le eccezioni, se non altrimenti specificato, sono di tipo *SimulationException* definita nel modulo *errors*.


## R1: Città e Villaggi
La classe astratta *Location* del modulo *locations*
rappresenta un luogo d'interesse per il quale si vuole valutare l'impatto della tempesta.
Essa definisce le property astratte:
- ```name(self) -> str```
- ```value(self) -> int```
- ```resilience(self) -> int```

Esse forniscono, rispettivamente, il nome, il valore architettonico, e la resistenza contro le intemperie del luogo d'interesse.
Considerare, senza controllarlo, che il valore della ```resilience``` sia sempre compreso tra 1 e 10.

La classe *TempestSimulator* del modulo *simulation* permette di definire città e villaggi.

Il metodo
```add_village(self, name: str, value: int, resilience: int) -> None```
permette di aggiungere un villaggio,
specificandone il nome, il valore architettonico, e la resistenza contro le intemperie.

Il metodo
```add_city(self, name: str, value: int, resilience: int) -> None```
permette di aggiungere una città,
specificandone il nome, il valore architettonico, e la resistenza contro le intemperie.

Il metodo
```get_location(self, name: str) -> Location```
permette di ottenere l'oggetto rappresentante un luogo d'interesse dato il nome.

Il metodo ``` __str__(self) -> str``` di *Location*,
restituisce la rappresentazione in stringa di un luogo d'interesse.
La stringa è composta dalla tipologia del luogo (*Village* o *City*) seguita dal suo nome, separati da uno spazio.
Esempi:
- *City Roma*
- *Village Gualtieri*


## R2: Calcolo danni
Il metodo astratto
```simulate_damage(self, intensity: float) -> float:``` della classe *Location*
permette di calcolare i danni al valore architettonico subiti da un luogo d'interesse
data l'intensità della tempesta che sia abbatte su di esso.
Considerare, senza controllarlo, che il valore d'intensità sia sempre compreso tra 1 e 10.

Il metodo astratto
```set_damage_function(self, damage_function: Callable[[float], float]) -> None``` della classe *Location*
permette d'impostare una **damage function** che, ottenuto il valore dell'intensità della tempesta,
restituisce un valore tra zero e uno,
rappresentante la percentuale di danni al valore architettonico subiti luogo d'interesse.
Questo metodo, se invocato su un oggetto rappresentante un villaggio, deve lanciare un'eccezione.

Il calcolo dei danni è diverso a seconda che il luogo d'interesse sia una città o un villaggio.

Per un villaggio la formula dei danni è la seguente:
```danni = valore_architettonico * (intensità - resistenza) / 10```.
Se la formula produce un risultato negativo, i danni sono subiti devono essere pari a zero.

Per una città, i danni subiti sono pari alla percentuale restituita dalla **damage function**,
moltiplicata per il valore architettonico della città,
**SOLAMENTE** nel caso in cui la resistenza della città sia inferiore all'intensità della tempesta.
In tutti gli altri casi, i danni sono pari a zero.

Nel caso in cui una **damage function** non sia impostata per la città
il metodo  ```simulate_damage``` lancia un'eccezione.


## R3: Zone a rischio
La classe *TempestSimulator* permette di rappresentare gli spostamenti della tempesta.

Il metodo
```set_next(self, location: str, next_location: str, attenuation: float) -> None```
accetta come primi due parametri i nomi di due luoghi d'interesse,
permettendo di specificare che, nel caso in cui una tempesta colpisse il primo,
il secondo sarebbe il prossimo a essere colpito.

La tempesta, spostandosi da un luogo a un altro, si riduce d'intensità.
La nuova intensità sarà pari all'intensità nel primo luogo,
moltiplicata per il fattore di attenuazione, fornito come terzo parametro.

**IMPORTANTE**: Si consideri che ogni luogo possa avere un unico precedente e un unico successivo.


Il metodo
```get_next(self, location: str) -> Optional[Tuple[Location, float]]```, dato il nome di un luogo d'interesse,
restituisce una *Tupla* contenente l'oggetto rappresentante il prossimo luogo colpito
e il valore del fattore di attenuazione dovuto allo spostamento tra i due luoghi.
Se non è stato definito il luogo successivo, il metodo deve restituire ```None```.


## R4: Simulazione
La classe TempestSimulator permette di simulare una tempesta.

Il metodo ```get_affected(self, start_location: str) -> List[Location]```
restituisce la lista di luoghi d'interesse colpiti dalla tempesta,
dato il nome del luogo di partenza.

Il metodo ```get_total_damage(self, start_location: str, intensity: float)```,
dato il nome del luogo di partenza e l'intensità di una tempesta,
restituisce la somma dei danni architettonici subiti dai luoghi d'interesse
incontrati dalla tempesta nel suo percorso.

**CONSIDERARE L'ATTENUAZIONE** dell'intensità della tempesta nello spostarsi da un luogo a quello successivo.


## R5: Imprevisti
Una tempesta può variare il suo percorso e colpire un luogo che non era stato previsto.

Il metodo  ```add_location(self, to_insert: str, location_before: str, attenuation: float) -> None```,
accetta il nome del luogo d'interesse da aggiungere al percorso della tempesta,
e il nome del luogo che lo precede.
Inserire il luogo d'interesse mantenendo inalterate le porzioni di percorso che lo seguono e lo precedono.

Si possono verificare **DUE CASI**:
- il luogo da aggiungere è nel mezzo del percorso.
- il luogo che precede quello da aggiungere è l'ultimo del percorso.

Nel primo caso, l'attenuazione della tempesta, fornita come terzo parametro,
è da considerarsi quella subita dalla tempesta nel passare la luogo inserito a quello successivo.
Le altre attenuazioni **NON** variano.

Nel secondo, il valore di attenuazione fornito come terzo parametro
è quello che subisce la tempesta nello spostarsi all'ultimo luogo inserito.