import matplotlib.pyplot as plt
import numpy as np
import random
import folium
from folium.plugins import TimestampedGeoJson

### class of location begin ###

class location:
    """
    class that determines location.

    name:str name of location
    loc:float(list) coordinates
    population:int number of people living in that location
    diff:int terrain difficulty
    resources:int(list) amount of resources
    belong:str which controls that location
    strat:int(list) importance for each side
    stan_walki:float current state of battle
    """
    def __init__(self, name="", loc=[0, 0], population=0, diff=0, resources=[0, 0, 0, 0], belong="", strat=[0, 0], stan_walki = 5):
        self.name = name  # nazwa
        self.loc = loc  # wspolrzedne [N+/ S-, W-/E+]
        self.population = population  # populacja
        self.diff = 0  # trudność terenu w tym wezle
        self.resources = resources  # jakie sa surowce [int(ropa), int(metale), int(technologie), int(metale_ziem_rzadkich)]
        self.belong = belong  # do kogo należy: ["usa", "chiny", ""]
        self.strat = strat  # poziom strategiczności dla usa/chiny [int(usa), int(chiny)]
        self.unit_list = []
        self.inbattle = False
        self.stan_walki = stan_walki
        self.bum=False
        self.bumbum=True
        self.trump = False
        self.bingchilling = False
        self.mnich = False
        self.puchatek = False
        self.tiananmen = False
        self.coronav2 = False

    def __str__(self):
        ans_list = {"name": self.name, "loc": self.loc, "population": self.population,
                    "diff": self.diff, "resources": self.resources,
                    "belong": self.belong,
                    "strategy": self.strat}
        return str(ans_list).replace(", '", ",\n")

    def get_neighbor(self, GraphEdges):
        """
        returns list of locations connected by route
        """
        ans_list = []
        for i in range(len(GraphEdges)):
            if self.name == GraphEdges[i].name1:
                ans_list.append([GraphEdges[i].name2, GraphEdges[i].distance, GraphEdges[i].diff])
            elif self.name == GraphEdges[i].name2:
                ans_list.append([GraphEdges[i].name1, GraphEdges[i].distance, GraphEdges[i].diff])
        return ans_list

    def get_neighbour_belong(self, GraphEdges):
        """
        returns list of locations connected by route
        """
        ans_list = []
        for i in range(len(GraphEdges)):
            if self.name == GraphEdges[i].name1:
                ans_list.append(
                    [GraphEdges[i].name2, GraphEdges[i].distance, GraphEdges[i].diff, GraphEdges[i].belong2])
            elif self.name == GraphEdges[i].name2:
                ans_list.append(
                    [GraphEdges[i].name1, GraphEdges[i].distance, GraphEdges[i].diff, GraphEdges[i].belong1])
        return ans_list


### class of loacation end ###

### class of route begin ###

class routte:
    """
    Class that determinates connections of locations class.

    distance:float distance between locations in 1000km
    diff:float(list) route difficulty
    name:str name of route
    name1:str name of first location
    name2:str name of second location
    belong1:str belongingness of first location
    belong2:str belongingness of second location
    """
    def __init__(self, loc1, loc2, diff=[0, 0, 0]):
        self.distance = self.haversine(loc1.loc, loc2.loc)  # dystans miedzy lokacjami w lini prostej w km
        self.diff = diff  # trudność terenu dla [int(ziemia), int(woda), int(powietrze)]
        self.name = loc1.name + " - " + loc2.name
        self.name1 = loc1.name
        self.name2 = loc2.name
        self.belong1 = loc1.belong
        self.belong2 = loc2.belong
        self.A = loc1
        self.B = loc2

    def haversine(self, A, B):
        """
        Return the distance between locations in thousands of kilometers
        """
        lon1, lat1, lon2, lat2 = A[1], A[0], B[1], B[0]
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        return 2 * 6 * np.arcsin(np.sqrt(a))  # 6371km przyblizone jako 6

    def __str__(self):
        return self.A.name + " -- " + str(self.distance) + " -- " + self.B.name


### class of route end ###

### map creating begin ###

SanDiego = location(name="San Diego",
                    loc=[32, -117],
                    population=3300000,
                    diff=1,
                    resources=[3, 7, 9, 0],
                    belong="usa",
                    strat=[10, 1])

Seattle = location(name="Seattle",
                   loc=[47, -122],
                   population=4000000,
                   diff=5,
                   resources=[5, 5, 9, 1],
                   belong="usa",
                   strat=[10, 1])

LosAlamos = location(name="Los Alamos",
                     loc=[36, -106],
                     population=100000,
                     diff=8,
                     resources=[7, 7, 10, 0],
                     belong="usa",
                     strat=[9, 0])

Honolulu = location(name="Pearl Harbour",
                    loc=[21, -158],
                    population=1000000,
                    diff=2,
                    resources=[0, 0, 0, 0],
                    belong="usa",
                    strat=[10, 4])

Hainan = location(name="Yulin",
                  loc=[18.2, 109.5],
                  population=9258000,
                  diff=1,
                  resources=[7, 6, 0, 2],
                  belong="chiny",
                  strat=[7, 7])

Maoming = location(name="Maoming",
                   loc=[21.6,110.91],
                   population=1272000,
                   diff=1,
                   resources=[5, 4, 1, 5],
                   belong="chiny",
                   strat=[6, 8])

Hsinchu = location(name="Hsinchu",
                   loc=[25.02, 121.38],
                   population=448207,
                   diff=1,
                   resources=[0, 2, 9, 0],
                   belong="",
                   strat=[10, 10])

Tainan = location(name="Tainan",
                  loc=[22.59, 120.11],
                  population=1881000,
                  diff=1,
                  resources=[0, 0, 7, 0],
                  belong="",
                  strat=[10, 10])

Philippnes = location(name="Philippines",
                      loc=[18.30, 122.08],
                      population=1881000,
                      diff=2,
                      resources=[0, 6, 7, 0],
                      belong="usa",
                      strat=[7, 6])

Guam = location(name="Guam",
                loc=[13.3, 144.4],
                population=170000,
                diff=5,
                resources=[0, 0, 0, 0],
                belong="usa",
                strat=[10, 8])

Pekin = location(name="Pekin",
                 loc=[40, 116],
                 population=22000000,
                 diff=2,
                 resources=[0, 0, 8, 0],
                 belong="chiny",
                 strat=[9, 10])

Shanghai = location(name="Shanghai",
                    loc=[31, 121.5],
                    population=27000000,
                    diff=1,
                    resources=[0, 0, 8, 0],
                    belong="chiny",
                    strat=[10, 10])

Fujian = location(name="Fujian",
                  loc=[25.8, 118],
                  population=38500000,
                  diff=1,
                  resources=[0, 4, 4, 8],
                  belong="chiny",
                  strat=[9, 8])

TaihangShan = location(name="Hebei",
                       loc=[37, 114],
                       population=74700000,
                       diff=8,
                       resources=[5, 9, 5, 7],
                       belong="chiny",
                       strat=[3, 9])

ThreeGorgesDam = location(name="Hubei",
                          loc=[31.2, 111.8],
                          population=58000000,
                          diff=8,
                          resources=[0, 3, 5, 0],
                          belong="chiny",
                          strat=[7, 10])

SychuanBasin = location(name="Sychuan",
                        loc=[30.9, 106.1],
                        population=83000000,
                        diff=10,
                        resources=[0, 8, 3, 8],
                        belong="chiny",
                        strat=[2, 7])

Korea_Polnocna = location(name="Korea Polnocna",
                          loc=[39.5, 126.7],
                          population=25970000,
                          diff=5,
                          resources=[0, 6, 1, 5],
                          belong="chiny",
                          strat=[8, 8])

Korea_Poludniowa = location(name="Korea Poludniowa",
                            loc=[36.2, 128.1],
                            population=51740000,
                            diff=5,
                            resources=[0, 7, 8, 5],
                            belong="usa",
                            strat=[8, 8])

Nagasaki = location(name="Kiusiu",
                    loc=[32.7, 131],
                    population=14311224,
                    diff=4,
                    resources=[0, 3, 6, 4],
                    belong="usa",
                    strat=[7, 6])

Kioto = location(name="South Honsiu",
                 loc=[34.7, 135.4],
                 population=25000000,
                 diff=6,
                 resources=[1, 5, 7, 5],
                 belong="usa",
                 strat=[7, 5])

Tokyo = location(name="North Honsiu",
                 loc=[36.6, 139.7],
                 population=35000000,
                 diff=5,
                 resources=[1, 6, 9, 4],
                 belong="usa",
                 strat=[9, 7])

Okinawa = location(name="Okinawa",
                   loc=[26.5, 127.9],
                   population=170000,
                   diff=5,
                   resources=[0, 1, 4, 0],
                   belong="usa",
                   strat=[8, 8])

GraphNodes = [SanDiego, Seattle, LosAlamos, Honolulu, Hainan, Maoming, Hsinchu, Tainan,
              Philippnes, Guam, Pekin, Shanghai, Fujian, TaihangShan, ThreeGorgesDam, SychuanBasin,
              Korea_Polnocna, Korea_Poludniowa, Nagasaki, Kioto, Tokyo, Okinawa]

GraphEdges = [routte(SanDiego, Seattle, [1, 1, 1]),
              routte(SanDiego, LosAlamos, [20, 10000, 2]),
              routte(Seattle, LosAlamos, [20, 10000, 2]),
              routte(SanDiego, Honolulu, [10000, 3, 3]),
              routte(Seattle, Honolulu, [10000, 3, 3]),
              routte(Honolulu, Guam, [10000, 3, 3]),
              routte(Guam, Philippnes, [10000, 2, 2]),
              routte(Philippnes, Tainan, [10000, 1, 1]),
              routte(Tainan, Hsinchu, [1, 1, 1]),
              routte(Philippnes, Hainan, [10000, 1, 1]),
              routte(Hainan, Maoming, [1, 1, 1]),
              routte(Tainan, Maoming, [1000, 1, 1]),
              routte(Korea_Polnocna, Tokyo, [1000, 1, 1]),
              routte(Maoming, ThreeGorgesDam, [2, 10000, 1]),
              routte(Maoming, Fujian, [1, 1, 1]),
              routte(Fujian, Hsinchu, [10000, 1, 1]),
              routte(ThreeGorgesDam, SychuanBasin, [5, 10000, 2]),
              routte(ThreeGorgesDam, Fujian, [1, 10000, 1]),
              routte(ThreeGorgesDam, TaihangShan, [4, 10000, 2]),
              routte(ThreeGorgesDam, Shanghai, [1, 10, 1]),
              routte(Fujian, Shanghai, [1, 1, 1]),
              routte(TaihangShan, Shanghai, [2, 10000, 1]),
              routte(Pekin, Shanghai, [1, 1, 1]),
              routte(Pekin, TaihangShan, [3, 10000, 2]),
              routte(SychuanBasin, TaihangShan, [6, 10000, 3]),
              routte(Honolulu, Tokyo, [10000, 2, 2]),
              routte(Tokyo, Kioto, [1, 1, 1]),
              routte(Guam, Kioto, [10000, 1, 1]),
              routte(Guam, Okinawa, [10000, 1, 1]),
              routte(Philippnes, Okinawa, [10000, 1, 1]),
              routte(Hsinchu, Okinawa, [10000, 1, 1]),
              routte(Tokyo, Kioto, [1, 1, 1]),
              routte(Tokyo, Korea_Poludniowa, [10000, 1, 1]),
              routte(Kioto, Korea_Poludniowa, [10000, 1, 1]),
              routte(Kioto, Nagasaki, [3, 1, 1]),
              routte(Okinawa, Nagasaki, [10000, 1, 1]),
              routte(Korea_Poludniowa, Nagasaki, [1, 1, 1]),
              routte(Korea_Poludniowa, Korea_Polnocna, [1, 1, 1]),
              routte(Pekin, Korea_Polnocna, [2, 1, 1]),
              routte(Okinawa,Tainan,[10000,1,2]),
              routte(Maoming,SychuanBasin,[2,2,2]),
              routte(Honolulu,Kioto,[10000,2,2])]

### map creating end ###

### class of militaryUnit begin ###

class militaryUnit:
    """
    Class of military unit

    belong:str to which country belong that unit
    name:str name of unit
    numbers:int(list) how many solders, tanks, planes and ships does unit have
    loc:lacation current location of unit
    destination_list:location(list) list of targets locations which unit want to takeover
    """
    def __init__(self, belong="", name="", numbers=[0, 0, 0, 0], loc=Honolulu, destination=Honolulu, destination_list=[]):
        self.belong = belong
        self.name = name
        self.numbers = np.array(numbers)
        self.hp = np.array([0, 0, 0, 0])
        self.dmg = np.array([0, 0, 0, 0])
        self.alive = True
        if belong == "usa":
            self.hp[0], self.hp[1] = numbers[0] * 1, numbers[1] * 8000
            self.hp[2], self.hp[3] = numbers[2] * 4000, numbers[3] * 25000
            self.dmg[0], self.dmg[1] = numbers[0] * 1, numbers[1] * 100
            self.dmg[2], self.dmg[3] = numbers[2] * 150, numbers[3] * 150
        elif belong == "china":
            self.hp[0], self.hp[1] = numbers[0] * 1, numbers[1] * 6500
            self.hp[2], self.hp[3] = numbers[2] * 2400, numbers[3] * 18000
            self.dmg[0], self.dmg[1] = numbers[0] * 1, numbers[1] * 85
            self.dmg[2], self.dmg[3] = numbers[2] * 90, numbers[3] * 140

        self.loc = loc
        self.inTravel = False  # na czas podróży wartość True
        self.inFight = False  # na czas uczestniczenia w bitwie wartość True
        self.unavailable_counter = 0  # odlicza czas w dniach ile jest jednostka niedostępna do odświeżenia
        self.destination_list = destination_list

    def __str__(self):
        ans_list = {"belong": self.belong, "name": self.name, "hp": self.hp, "dmg": self.dmg, "loc": self.loc.name,
                    "inTravel": self.inTravel, "inFight": self.inFight, "Unavailable for": self.unavailable_counter}
        return str(ans_list).replace(", '", ",\n")

    def day_gone(self, ):  # ta funkcja będzie włączana dla każdej jednostki raz dziennie
        """
        Checks state of unit every time stample
        """
        if self.unavailable_counter > 1:
            self.unavailable_counter -= 1
        elif self.unavailable_counter == 1:
            self.unavailable_counter = 0
            self.inTravel = False
            self.inFight = False
        elif self.unavailable_counter == 0:
            self.inTravel = False
            self.inFight = False

        for j in range(len(self.hp)):
            if self.hp[j] < 0:
                self.hp[j] = 0

        if sum(self.hp) <= 0:
            self.alive = False

        for j in range(len(self.numbers)):
            if self.numbers[j] < 0:
                self.numbers[j] = 0

    def where2go(self, GraphEdges=GraphEdges):
        """
        Returns a three-element list: name of the destination, cost to reach the destination, duration of the journey
        """
        destination_list = self.loc.get_neighbor(GraphEdges)
        costs_list = destination_list
        return_list = []
        for i in range(len(destination_list)):
            costs_list[i].append(
                [destination_list[i][2][0] * self.hp[0] * destination_list[i][1] * 0.01,  # ziemia - piechota
                 destination_list[i][2][0] * self.hp[1] * destination_list[i][1] * 0.01,  # ziemia - czolg
                 destination_list[i][2][2] * self.hp[2] * destination_list[i][1] * 0.01,  # powietrze - samolot
                 destination_list[i][2][1] * self.hp[3] * destination_list[i][1] * 0.01])  # morze - okret
            return_list.append([costs_list[i][0], sum(costs_list[i][3]), np.ceil(destination_list[i][1])])
        return return_list

    def check_neighbour(self, GraphEdges=GraphEdges, GraphNodes=GraphNodes):
        """
        Checks where to go in random walk variant.
        """
        if self.alive:
            destination_list = self.loc.get_neighbour_belong(GraphEdges)
            can_attack = []
            if self.belong == "usa":
                for i in destination_list:
                    if i[3] == "china":
                        can_attack.append(i[0])
            elif self.belong == "china":
                for i in destination_list:
                    if i[3] == "usa":
                        can_attack.append(i[0])
            ans_list = []
            if len(can_attack) == 0:
                for i in destination_list:
                    can_attack.append(i[0])
            for Node in GraphNodes:
                for name in can_attack:
                    if name == Node.name:
                        ans_list.append(Node)
            ### attack
            self.move(np.random.choice(ans_list))

    def check_neighbour_random_waits03(self, GraphEdges=GraphEdges, GraphNodes=GraphNodes):
        """
        Checks where to go in random walk variant.
        """
        if self.alive:
            destination_list = self.loc.get_neighbour_belong(GraphEdges)
            can_attack = []

            china_woj = []
            for i in china_units:
                if i.alive == True:
                    china_woj.append(i.loc)

            usa_woj = []
            for i in usa_units:
                if i.alive == True:
                    usa_woj.append(i.loc)

            if self.belong == "usa":
                for i in destination_list:
                    if i[3] == "china":
                        can_attack.append(i[0])
            elif self.belong == "china":
                for i in destination_list:
                    if i[3] == "usa":
                        can_attack.append(i[0])
            ans_list = []
            if len(can_attack) == 0:
                for i in destination_list:
                    can_attack.append(i[0])
            for Node in GraphNodes:
                for name in can_attack:
                    if name == Node.name:
                        ans_list.append(Node)
            ### attack
            if np.random.random() < 0.5 and self.belong == "usa":
                if ThreeGorgesDam.bum==True and ThreeGorgesDam in ans_list:
                    ans_list.remove(ThreeGorgesDam)
                if SychuanBasin in ans_list:
                    ans_list.remove(SychuanBasin)
                if Honolulu in ans_list:
                    ans_list.remove(Honolulu)
                wh = np.random.choice(ans_list)
                if wh not in usa_woj:
                    self.move(wh)
            elif np.random.random() < 0.8 and self.belong == "china":
                if ThreeGorgesDam.bum==True and ThreeGorgesDam in ans_list:
                    ans_list.remove(ThreeGorgesDam)
                if Honolulu in ans_list:
                    ans_list.remove(Honolulu)
                wh=np.random.choice(ans_list)
                if wh not in china_woj:
                    self.move(wh)

    def check_neighbour_random_waits03_2(self, GraphEdges=GraphEdges, GraphNodes=GraphNodes):
        """
        Checks where to go in random walk variant.
        """
        if self.alive:
            destination_list = self.loc.get_neighbour_belong(GraphEdges)
            can_attack = []

            china_woj = []
            for i in china_units:
                if i.alive == True:
                    china_woj.append(i.loc)

            usa_woj = []
            for i in usa_units:
                if i.alive == True:
                    usa_woj.append(i.loc)

            if self.belong == "usa":
                for i in destination_list:
                    if i[3] == "china":
                        can_attack.append(i[0])
            elif self.belong == "china":
                for i in destination_list:
                    if i[3] == "usa":
                        can_attack.append(i[0])
            ans_list = []
            if len(can_attack) == 0:
                for i in destination_list:
                    can_attack.append(i[0])
            for Node in GraphNodes:
                for name in can_attack:
                    if name == Node.name:
                        ans_list.append(Node)
            ### attack
            if np.random.random() < 0.3 and self.belong == "usa":
                if ThreeGorgesDam.bum==True and ThreeGorgesDam in ans_list:
                    ans_list.remove(ThreeGorgesDam)
                if SychuanBasin in ans_list:
                    ans_list.remove(SychuanBasin)
                if Honolulu in ans_list:
                    ans_list.remove(Honolulu)
                wh = np.random.choice(ans_list)
                self.move(wh)
            elif np.random.random() < 0.3 and self.belong == "china":
                if ThreeGorgesDam.bum==True and ThreeGorgesDam in ans_list:
                    ans_list.remove(ThreeGorgesDam)
                if Honolulu in ans_list:
                    ans_list.remove(Honolulu)
                wh=np.random.choice(ans_list)
                self.move(wh)


    def move(self, destination):
        """
        Moves a unit to the given destination
        """

        if not self.inTravel and not self.inFight:
            list_of_directions = self.where2go()
            for i in range(len(list_of_directions)):
                if list_of_directions[i][0] == destination.name:
                    self.unavailable_counter = list_of_directions[i][2]
                    self.loc = destination
                    self.inTravel = True
                    break

    def fronty_ale_to_chodzi(self, GraphEdges=GraphEdges, GraphNodes=GraphNodes):
        """
        Controls unit movements using self.destination_list
        """
        if self.alive:
            if ThreeGorgesDam.bum==True:
                if ThreeGorgesDam in self.destination_list:
                    self.destination_list.remove(ThreeGorgesDam)
            china_woj = []
            for i in china_units:
                if i.alive==True:
                    china_woj.append(i.loc)

            usa_woj = []
            for i in usa_units:
                if i.alive == True:
                    usa_woj.append(i.loc)
            if self.loc==self.destination_list[-1] or self.loc not in self.destination_list:
                self.check_neighbour_random_waits03()


            elif (self.destination_list[self.destination_list.index(self.loc)+1] not in usa_woj and self.belong=="usa") or (self.destination_list[self.destination_list.index(self.loc)+1] not in china_woj and self.belong=="china"):
                if  (self.loc not in china_woj and self.belong=="usa") or (self.loc not in usa_woj and self.belong=="china"):
                    self.move(self.destination_list[self.destination_list.index(self.loc)+1])

    def fronty_ale_to_chodzi2(self, GraphEdges=GraphEdges, GraphNodes=GraphNodes):
        """
        Controls unit movements using self.destination_list
        """
        if self.alive:
            if ThreeGorgesDam.bum==True:
                if ThreeGorgesDam in self.destination_list:
                    self.destination_list.remove(ThreeGorgesDam)
            china_woj = []
            for i in china_units:
                if i.alive==True:
                    china_woj.append(i.loc)

            usa_woj = []
            for i in usa_units:
                if i.alive == True:
                    usa_woj.append(i.loc)
            if self.loc==self.destination_list[-1] or self.loc not in self.destination_list:
                self.check_neighbour_random_waits03_2()


            else:
                if (self.loc not in china_woj and self.belong=="usa") or (self.loc not in usa_woj and self.belong=="china"):
                    self.move(self.destination_list[self.destination_list.index(self.loc)+1])


### class of militaryUnit end ###

### init militaryUnits begin ###

china1 = militaryUnit(belong="china", name="1", numbers=[10000, 50, 100, 0], loc=SychuanBasin, destination_list=[SychuanBasin])
china2 = militaryUnit(belong="china", name="2", numbers=[125000, 100, 100, 0], loc=TaihangShan, destination_list=[TaihangShan,Pekin,Korea_Polnocna,Korea_Poludniowa,Tokyo])
china3 = militaryUnit(belong="china", name="3", numbers=[225000, 200, 300, 100], loc=Pekin, destination_list=[Pekin,Korea_Polnocna,Korea_Poludniowa,Tokyo])
china4 = militaryUnit(belong="china", name="4", numbers=[350000, 250, 300, 100], loc=Korea_Polnocna, destination_list=[Korea_Polnocna,Korea_Poludniowa,Tokyo])
china5 = militaryUnit(belong="china", name="5", numbers=[115000, 150, 200, 0], loc=ThreeGorgesDam, destination_list=[ThreeGorgesDam,Shanghai, Fujian, Hsinchu, Tainan, Okinawa, Nagasaki, Kioto])
china6 = militaryUnit(belong="china", name="6", numbers=[150000, 300, 300, 100], loc=Shanghai, destination_list=[Shanghai,Fujian, Hsinchu, Tainan, Okinawa, Nagasaki, Kioto])
china7 = militaryUnit(belong="china", name="7", numbers=[200000, 300, 500, 200], loc=Fujian, destination_list=[Fujian, Hsinchu, Tainan, Okinawa, Nagasaki, Kioto])
china8 = militaryUnit(belong="china", name="8", numbers=[125000, 150, 100, 50], loc=Maoming, destination_list=[Maoming,Hainan, Philippnes, Guam])
china9 = militaryUnit(belong="china", name="9", numbers=[110000, 100, 500, 150], loc=Hainan, destination_list=[Hainan,Philippnes, Guam])

usa1 = militaryUnit(belong="usa", name="1", numbers=[20000, 200, 400, 0], loc=LosAlamos, destination_list=[LosAlamos,SanDiego,Honolulu,Guam,Philippnes,Hainan,Maoming])
usa2 = militaryUnit(belong="usa", name="2", numbers=[50000, 300, 400, 30], loc=Seattle, destination_list=[Seattle,Honolulu,Kioto,Nagasaki,Okinawa,Tainan,Hsinchu,Fujian,Shanghai,ThreeGorgesDam])
usa3 = militaryUnit(belong="usa", name="3", numbers=[50000, 300, 400, 40], loc=SanDiego, destination_list=[SanDiego,Honolulu,Tokyo,Korea_Poludniowa,Korea_Polnocna,Pekin,TaihangShan])
usa4 = militaryUnit(belong="usa", name="4", numbers=[20000, 50, 600, 100], loc=Honolulu, destination_list=[Honolulu,Kioto,Nagasaki,Okinawa,Tainan,Hsinchu,Fujian,Shanghai,ThreeGorgesDam])
usa5 = militaryUnit(belong="usa", name="5", numbers=[20000, 20, 400, 30], loc=Guam, destination_list=[Guam,Philippnes,Hainan,Maoming])
usa6 = militaryUnit(belong="usa", name="6", numbers=[20000, 50, 400, 20], loc=Philippnes, destination_list=[Philippnes,Hainan,Maoming])
usa7 = militaryUnit(belong="usa", name="7", numbers=[20000, 60, 200, 20], loc=Tainan, destination_list=[Tainan,Hsinchu,Fujian,Shanghai,ThreeGorgesDam])
usa8 = militaryUnit(belong="usa", name="8", numbers=[20000, 60, 200, 20], loc=Hsinchu, destination_list=[Hsinchu,Fujian,Shanghai,SychuanBasin])
usa9 = militaryUnit(belong="usa", name="9", numbers=[150000, 150, 400, 100], loc=Tokyo, destination_list=[Tokyo,Korea_Poludniowa,Korea_Polnocna,Pekin,TaihangShan])
usa10 = militaryUnit(belong="usa", name="10", numbers=[100000, 100, 400, 50], loc=Kioto, destination_list=[Kioto,Nagasaki,Okinawa,Tainan,Hsinchu,Fujian,Shanghai,ThreeGorgesDam])
usa11 = militaryUnit(belong="usa", name="12", numbers=[100000, 150, 400, 50], loc=Nagasaki, destination_list=[Nagasaki,Okinawa,Tainan,Hsinchu,Fujian,Shanghai,ThreeGorgesDam])
usa12 = militaryUnit(belong="usa", name="12", numbers=[10000, 30, 300, 40], loc=Okinawa, destination_list=[Okinawa,Tainan,Hsinchu,Fujian,Shanghai,ThreeGorgesDam])
usa13 = militaryUnit(belong="usa", name="13", numbers=[20000, 150, 200, 50], loc=Korea_Poludniowa, destination_list=[Korea_Poludniowa,Korea_Polnocna,Pekin,TaihangShan])

usa_units = [usa1, usa2, usa3, usa4, usa5, usa6, usa7, usa8, usa9, usa10, usa11, usa12, usa13]
china_units = [china1, china2, china3, china4, china5, china6, china7, china8, china9]


### init militaryUnits end ###

### battle begin ###

def day_battle(liczby_us, liczby_ch, atakujacy,loc):
    """
    Returns:
        numbers of US unit:float(array)
        numbers of China unit:float(array)
        hp of US unit:float
        hp of China unit:float
    """
    piechota_us = [1, 1]
    czolg_us = [8000, 100]
    samolot_us = [4000, 150]
    statek_us = [25000, 150]

    piechota_ch = [1, 1]
    czolg_ch = [6500, 85]
    samolot_ch = [2400, 130]
    statek_ch = [18000, 140]

    for i in range(len(liczby_ch)):
        if np.isnan(liczby_ch[i]):
            liczby_ch[i] = 0
        if np.isnan(liczby_us[i]):
            liczby_us[i] = 0

    hp_us = piechota_us[0] * liczby_us[0] + czolg_us[0] * liczby_us[1] + samolot_us[0] * liczby_us[2] + statek_us[0] * \
            liczby_us[3]
    dmg_us = piechota_us[1] * liczby_us[0] + czolg_us[1] * liczby_us[1] + samolot_us[1] * liczby_us[2] + statek_us[1] * \
             liczby_us[3]

    procent_piech_us = liczby_us[0] / hp_us
    procent_czolg_us = liczby_us[1] / hp_us
    procent_samolot_us = liczby_us[2] / hp_us
    procent_statek_us = liczby_us[3] / hp_us

    hp_ch = piechota_ch[0] * liczby_ch[0] + czolg_ch[0] * liczby_ch[1] + samolot_ch[0] * liczby_ch[2] + statek_ch[0] * \
            liczby_ch[3]
    dmg_ch = piechota_ch[1] * liczby_ch[0] + czolg_ch[1] * liczby_ch[1] + samolot_ch[1] * liczby_ch[2] + statek_ch[1] * \
             liczby_ch[3]

    procent_piech_ch = liczby_ch[0] / hp_ch
    procent_czolg_ch = liczby_ch[1] / hp_ch
    procent_samolot_ch = liczby_ch[2] / hp_ch
    procent_statek_ch = liczby_ch[3] / hp_ch

    hp_us_pocz = hp_us
    hp_ch_pocz = hp_ch
    stan_walki = 5
    dzien = 0

    if loc.belong == "usa":
        pips = [random.randint(2, 6), random.randint(1, 5)]
    else:
        pips = [random.randint(1, 5), random.randint(2, 6)]

    trzesienie = random.randint(1, 10000)

    if atakujacy == "USA":
        hp_ch2 = hp_ch - dmg_us * pips[0]
        dmg_ch = dmg_ch * (hp_ch2 / hp_ch)
        hp_ch = hp_ch2

        hp_us2 = hp_us - dmg_ch * pips[1]
        dmg_us = dmg_us * (hp_us2 / hp_us)
        hp_us = hp_us2
    else:
        hp_us2 = hp_us - dmg_ch * pips[1]
        dmg_us = dmg_us * (hp_us2 / hp_us)
        hp_us = hp_us2

        hp_ch2 = hp_ch - dmg_us * pips[0]
        dmg_ch = dmg_ch * (hp_ch2 / hp_ch)
        hp_ch = hp_ch2

    if trzesienie == 69:
        print("Trzesienie ziemi")
        hp_us = hp_us / 2
        dmg_us = dmg_us / 2
        hp_ch = hp_ch / 2
        dmg_ch = dmg_ch / 2

    if hp_us < 0:
        hp_us = 0

    if hp_ch < 0:
        hp_ch = 0



    liczby_us_koniec = [int(procent_piech_us * hp_us), int(procent_czolg_us * hp_us), int(procent_samolot_us * hp_us),
                        int(procent_statek_us * hp_us)]
    liczby_ch_koniec = [int(procent_piech_ch * hp_ch), int(procent_czolg_ch * hp_ch), int(procent_samolot_ch * hp_ch),
                        int(procent_statek_ch * hp_ch)]

    for i in range(len(liczby_ch_koniec)):
        if liczby_ch_koniec[i] <= 0:
            liczby_ch_koniec[i] = 0
    for i in range(len(liczby_us_koniec)):
        if liczby_us_koniec[i] <= 0:
            liczby_us_koniec[i] = 0

    return np.array(liczby_us_koniec), np.array(liczby_ch_koniec), hp_us, hp_ch


def battle_units(usa_unit, china_unit):
    stan_walki = 5
    c, d = np.sum(usa_unit.hp), np.sum(china_unit.hp)
    i = 0
    if usa_unit.unavailable_counter == 0 and china_unit.unavailable_counter == 0 and usa_unit.loc == china_unit.loc and china_unit.alive and usa_unit.alive:
        while 0 < stan_walki < 10 and c > 0 and d > 0:
            a, b, c, d = day_battle(usa_unit.numbers, china_unit.numbers, np.random.choice(["USA", "Chiny"]),usa_unit.loc)
            usa_unit.numbers, usa_unit.hp = a, np.array([a[0] * 1, a[1] * 8000, a[2] * 4000, a[3] * 25000])
            china_unit.numbers, china_unit.hp = b, np.array([b[0] * 1, b[1] * 6500, b[2] * 2400, b[3] * 18000])
            if c == 0:
                stan_walki = 0
                usa_unit.alive = False
            elif d == 0:
                stan_walki = 10
                china_unit.alive = False
            else:
                stan_walki = stan_walki + c / d - d / c
            i += 1
        if stan_walki >= 10:
            usa_unit.loc.belong = "usa"
        elif stan_walki <= 0:
            usa_unit.loc.belong = "chiny"

        usa_unit.unavailable_counter = i
        china_unit.unavailable_counter = i
        usa_unit.inFight = True
        china_unit.inFight = True

### battle end ###

### battle v2 begin ###

def check_battle_parameters(loc,units_us,units_ch):
    """
    Controls function battle_multiple_units
    """
    ans_us = []
    ans_ch = []
    for i in units_us:
        if i.unavailable_counter == 0 and i.loc == loc and i.alive:
            ans_us.append(i)

    for i in units_ch:
        if i.unavailable_counter == 0 and i.loc == loc and i.alive:
            ans_ch.append(i)

    if len(ans_us) >= 1 and len(ans_ch) >= 1:
        battle_multiple_units(ans_us,ans_ch,loc,loc.stan_walki)

def battle_multiple_units(usa_unit_list, china_unit_list,loc,stan_walki = 5):
    """
    Controls battle of many military units
    """
    numbers_us = np.array([0.0, 0.0, 0.0, 0.0])
    numbers_ch = np.array([0.0, 0.0, 0.0, 0.0])
    hp_us = 0
    hp_ch = 0
    for i in usa_unit_list:
        numbers_us += i.numbers
        hp_us += np.sum(i.hp)
        i.unavailable_counter = 1
        i.inFight = True
    for i in china_unit_list:
        numbers_ch += i.numbers
        hp_ch += np.sum(i.hp)
        i.unavailable_counter = 1
        i.inFight = True

    c, d = hp_us, hp_ch

    if 0 < stan_walki < 10 and hp_us > 0 and hp_ch > 0:
        a, b, c, d = day_battle(numbers_us, numbers_ch, np.random.choice(["USA", "Chiny"]),loc)

        for i in usa_unit_list:
            i.numbers, i.hp = a*1/len(usa_unit_list), np.array([a[0] * 1, a[1] * 8000, a[2] * 4000, a[3] * 25000])*1/len(usa_unit_list)
            for j in range(len(i.numbers)):
                if i.numbers[j] < 0:
                    i.numbers[j] = 0
        for i in china_unit_list:
            i.numbers, i.hp = b*1/len(china_unit_list), np.array([b[0] * 1, b[1] * 6500, b[2] * 2400, b[3] * 18000])*1/len(china_unit_list)
            for j in range(len(i.numbers)):
                if i.numbers[j] < 0:
                    i.numbers[j] = 0

    if c <= 0:
        stan_walki = 0
        for i in usa_unit_list:
            i.alive = False
    elif d <= 0:
        stan_walki = 10
        for i in china_unit_list:
            i.alive = False
    else:
        stan_walki = stan_walki + c / d - d / c

    loc.stan_walki = stan_walki

    if stan_walki >= 10:
        loc.belong = "usa"
        loc.stan_walki = 5.0
    elif stan_walki <= 0:
        loc.belong = "chiny"
        loc.stan_walki = 5.0

### battle v2 end ###

### all war management begin ###

def main(usa_unit, china_unit):
    """
    Simulate war (military units movement on map)
    """
    for i in range(1000):
        if i%10 == 0:
            usa_units.append(militaryUnit(belong="usa", name=str(i), numbers=[5000, 10, 50, 15], loc=LosAlamos))
            china_units.append(militaryUnit(belong="usa", name=str(i), numbers=[15000, 10, 50, 15], loc=SychuanBasin))
        us_alive_counter, ch_alive_counter = 0, 0

        for j in usa_units:
            j.check_neighbour()
            j.day_gone()
            us_alive_counter += j.alive
        for j in china_units:
            j.check_neighbour()
            j.day_gone()
            ch_alive_counter += j.alive
        # for j in usa_units:
        #     for k in china_units:
        #         battle_units(j, k)

        for j in GraphNodes:
            check_battle_parameters(j,usa_units,china_units)

        print("day " + str(i),
              "USA: " + str(us_alive_counter) + "/" + str(len(usa_units)),
              "CHINA: " + str(ch_alive_counter) + "/" + str(len(china_units)))

        if us_alive_counter == 0 or ch_alive_counter == 0: return i, us_alive_counter, ch_alive_counter


### begining of Economy zone ###

def Economy(peace=False, i=0, GDPu=[23.06], GDPc=[15.73], Cu=[15.36], Iu=[4.36], Gu=[4.04], Tu=[-0.70], Cc=[9.33],
            Ic=[5.67], Gc=[0.67], Tc=[0.06], usa_uni=[], china_uni=[]):
    """
    Simulate GDP during war and peace
    """
    # GDPu = [23.06]
    # GDPc = [15.73]
    # Cu, Iu, Gu, Tu = [15.36], [4.36], [4.04], [-0.70]
    # au, bu, cu, du, eu, fu, gu, hu, ku = 0.06, 0.02, 0.02, 0.01, 0.01, 0.03, 0.02, 0.01, -0.005
    # Cc, Ic, Gc, Tc = [9.33], [5.67], [0.67], [0.06]
    # ac, bc, cc, dc, ec, fc, gc, hc, kc = 0.05, 0.001, 0.03, 0.005, 0.03, 0.1, 0.04, 0.02, 0.2
    if peace == True:
        au, bu, cu, du, eu, fu, gu, hu, ku = 0.06 / 195, 0.02 / 195, 0.02 / 195, 0.01 / 195, 0.01 / 195, 0.03 / 195, 0.02 / 195, 0.01 / 195, -0.005 / 195
        ac, bc, cc, dc, ec, fc, gc, hc, kc = 0.05 / 195, 0.001 / 195, 0.03 / 195, 0.005 / 195, 0.03 / 195, 0.1 / 195, 0.04 / 195, 0.02 / 195, 0.2 / 195
    else:
        au, bu, cu, du, eu, fu, gu, hu, ku = 0.01 / 195, 0.04 / 195, 0.001 / 195, 0.01 / 195, 0.1 / 195, 0.06 / 195, 0.03 / 195, 0.01 / 195, 0.01 / 195
        ac, bc, cc, dc, ec, fc, gc, hc, kc = 0.03 / 195, 0.05 / 195, 0.03 / 195, 0.005 / 195, 0.12 / 195, 0.05 / 195, 0.02 / 195, 0.01 / 195, 0.2 / 195

    # dodatkowe współczynniki dla spadku handlu
    USA_handel, Chiny_handel = 0, 0

    if peace == False:
        USA_handel = -1.3 / 195
        Chiny_handel = -0.65 / 195
    x = 0
    d = 0

    for j in usa_uni:
        liczby = j.numbers
        if j.alive == True:
            x = x + liczby[0]*1000/10**12 + liczby[1]*24*15000/10**12 + liczby[2]*17600*24/10**12 + liczby[2]*160000*24/10**12
    
    
    for j in china_uni:
        liczby = j.numbers
        if j.alive == True:
            d = d + liczby[0]*500/10**12 + liczby[1]*24*12000/10**12 + liczby[2]*14600*24/10**12 + liczby[2]*130000*24/10**12

    if ThreeGorgesDam.bum == True and ThreeGorgesDam.bumbum == True:
        Chiny_handel = -2.15 / 195
    
    if LosAlamos.trump == True:
        USA_handel = USA_handel - 0.3 / 195
    
    if Pekin.bingchilling == True:
        Chiny_handel = Chiny_handel + 0.2 / 195

    if SychuanBasin.mnich == True:
        Chiny_handel = Chiny_handel + 0.1 / 195

    if Pekin.puchatek == True:
        Chiny_handel = Chiny_handel - 0.05 / 195

    if Pekin.tiananmen == True:
        Chiny_handel = Chiny_handel - 0.2 / 195

    if Pekin.coronav2 == True:
        Chiny_handel = Chiny_handel - 1 / 195
    

    dCu = au * Cu[i - 1] - bu * GDPu[i - 1]
    dIu = cu * GDPu[i - 1] - du * Iu[i - 1]
    dGu = eu * Gu[i - 1]
    dTu = 0
    dGDPu = fu * Cu[i - 1] + gu * Iu[i - 1] + hu * Gu[i - 1] + ku * Tu[i - 1] + USA_handel
    Cu.append(Cu[i - 1] + dCu)
    Iu.append(Iu[i - 1] + dIu)
    Gu.append(Gu[i - 1] + dGu + x)
    # Tu.append(Tu[i-1] + dTu)
    GDPu.append(GDPu[i - 1] + dGDPu)
    Tu.append(GDPu[i] - Cu[i] - Iu[i] - Gu[i])

    dCc = ac * Cc[i - 1] - bc * GDPc[i - 1]
    dIc = cc * GDPc[i - 1] - dc * Ic[i - 1]
    dGc = ec * Gc[i - 1]
    dTc = 0
    dGDPc = fc * Cc[i - 1] + gc * Ic[i - 1] + hc * Gc[i - 1] + kc * Tc[i - 1] + Chiny_handel
    # Tu.append(Tu[i-1] + dTu)
    Cc.append(Cc[i - 1] + dCc)
    Ic.append(Ic[i - 1] + dIc)

    Gc.append(Gc[i - 1] + dGc + d)

    GDPc.append(GDPc[i - 1] + dGDPc)
    Tc.append(GDPc[i] - Cc[i] - Ic[i] - Gc[i])

    # if Cu[i] <= 2.1 or Cc[i] <= 1.2:  # zbyt mała konsumpcja na kontynuacje wojny
    #     return -1000, -1000
    # if Iu[i] <= 0 or Ic[i] <= 0:  # zbyt mała produkcja na kontynuacje wojny
    #     return -1000, -1000
    # if Gu[i] <= -2 or Gc[i] <= -2:  # zbyt duże rośnięcie długu publicznego ####################### do przemyślenia
    #     return -100000, -100000

    GDPu_peace, GDPc_peace = GDPu, GDPc

    return GDPu_peace, GDPc_peace

### end of Economy zone ###

Usa360=[Seattle, LosAlamos, SanDiego, Honolulu]
def main2(usa_unit, china_unit):
    """
    Simulate war (military units movement on map)
    """
    obiekty = []

    for i in range(1000):

        GDPu, GDPc = Economy(peace=False, i=i, usa_uni = usa_unit, china_uni = china_unit)


        if i%50 == 49:
            xd = np.random.random()
            if 0<=xd<1/3:

                usa_units.append(militaryUnit(belong="usa", name=str(int(i/10+13)), numbers=[5000, 10, 50, 15], loc=LosAlamos, destination_list=[LosAlamos,SanDiego,Honolulu,Guam,Philippnes,Hainan,Maoming]))
                china_units.append(militaryUnit(belong="china", name=str(int(i/10+9)), numbers=[15000, 50, 50, 10],loc=SychuanBasin, destination_list=[SychuanBasin,TaihangShan,Pekin,Korea_Polnocna,Korea_Poludniowa,Tokyo]))
            elif 1/3 <= xd < 2/3:
                usa_units.append(militaryUnit(belong="usa", name=str(int(i/10+13)), numbers=[5000, 10, 50, 15], loc=Seattle, destination_list = [Seattle, Honolulu, Kioto, Nagasaki, Okinawa, Tainan, Hsinchu, Fujian, Shanghai]))
                china_units.append(militaryUnit(belong="china", name=str(int(i/10+9)), numbers=[15000, 50, 50, 10], loc=SychuanBasin, destination_list=[SychuanBasin]))
            else:
                usa_units.append(militaryUnit(belong="usa", name=str(int(i/10+13)), numbers=[5000, 10, 50, 15], loc=SanDiego, destination_list=[SanDiego,Honolulu,Tokyo,Korea_Poludniowa,Korea_Polnocna,Pekin,TaihangShan]))
                china_units.append(militaryUnit(belong="china", name=str(int(i/10+9)), numbers=[15000, 50, 50, 10], loc=Maoming, destination_list=[Maoming,Hainan, Philippnes, Guam]))
        for j in usa_units:
            if j.loc==ThreeGorgesDam and j.inTravel==False:
                ThreeGorgesDam.bum=True
                j.alive = False

        u = np.random.random()
        if u < 0.001:
            LosAlamos.trump = True
            print('trump')

        if u > 0.001 and u < 0.003:
            Pekin.bingchilling = True
            print('bingchilling')

        if u > 0.005 and u < 0.009:
            SychuanBasin.mnich = True
            print('mnich')

        if u > 0.15 and u < 0.17:
            Pekin.puchatek = True
            print('puchatek')

        if u < 0.5 and u > 0.499:
            Pekin.coronav2 = True
            print('coronav2')

        obiekty.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [170, 50]
            },
            'properties': {
                "time": 1.68493 * 10 ** 12 + 86400000 * i,
                'popup': "USA: " + str(GDPu[i]),
                'icon': 'marek', 'iconstyle': {'color': 'blue', 'stroke': 'true', 'fillOpacity': 0.3}
            }
        })
        obiekty.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [160, 50]
            },
            'properties': {
                "time": 1.68493 * 10 ** 12 + 86400000 * i,
                'popup': "Chiny: " + str(GDPc[i]),
                'icon': 'marek', 'iconstyle': {'color': 'red', 'stroke': 'true', 'fillOpacity': 0.3}
            }
        })
        if ThreeGorgesDam.bum==True:
            obiekty.append({
                            'type': 'Feature',
                            'geometry': {
                                'type': 'Point',
                                'coordinates': [ThreeGorgesDam.loc[1], ThreeGorgesDam.loc[0]]
                            },
                            'properties': {
                                "time": 1.68493 * 10 ** 12 + 86400000 * i,
                                'popup': str("Tama bum!!!"),
                                'icon': 'circle', 'iconstyle': {'color': 'green', 'stroke': 'true', 'fillOpacity': 0.3}
                            }
                        })

        for jednostka in usa_units:
            if jednostka.alive == True:
                if jednostka.inFight == True:
                    if (jednostka.loc in Usa360):
                        cord1, cord2 = jednostka.loc.loc[1] + 360, jednostka.loc.loc[0]
                    else:
                        cord1, cord2 = jednostka.loc.loc[1], jednostka.loc.loc[0]
                    obiekty.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [cord1, cord2]
                        },
                        'properties': {
                            "time": 1.68493 * 10 ** 12 + 86400000 * i,
                            'popup': str(jednostka.name),
                            'icon': 'circle', 'iconstyle': {'color': 'black', 'stroke': 'true', 'fillOpacity': 1}
                        }
                    })
                else:
                    if (jednostka.loc in Usa360):
                        cord1, cord2 = jednostka.loc.loc[1] + 360, jednostka.loc.loc[0]
                    else:
                        cord1, cord2 = jednostka.loc.loc[1], jednostka.loc.loc[0]
                    obiekty.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [cord1, cord2]
                        },
                        'properties': {
                            "time": 1.68493*10**12+86400000* i,
                            'popup': str(jednostka),
                            'icon': 'circle', 'iconstyle': {'color': 'blue'}
                        }
                    })
            else:
                continue
        for jednostka in china_units:
            if jednostka.alive == True:
                if jednostka.inFight == True:
                    if (jednostka.loc in Usa360):
                        cord1, cord2 = jednostka.loc.loc[1] + 360, jednostka.loc.loc[0]
                    else:
                        cord1, cord2 = jednostka.loc.loc[1], jednostka.loc.loc[0]
                    obiekty.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [cord1, cord2]
                        },
                        'properties': {
                            "time": 1.68493 * 10 ** 12 + 86400000 * i,
                            'popup': str(jednostka.name),
                            'icon': 'circle', 'iconstyle': {'color': 'black', 'stroke': 'true', 'fillOpacity': 1}
                        }
                    })
                else:
                    if (jednostka.loc in Usa360):
                        cord1, cord2 = jednostka.loc.loc[1] + 360, jednostka.loc.loc[0]
                    else:
                        cord1, cord2 = jednostka.loc.loc[1], jednostka.loc.loc[0]
                    obiekty.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [cord1, cord2]
                        },
                        'properties': {
                            "time": 1.68493*10**12+86400000* i,
                            'popup': str(jednostka),
                            'icon': 'circle', 'iconstyle': {'color': 'red'}
                        }
                    })
            else:
                continue

        us_alive_counter, ch_alive_counter = 0, 0
        u=random.random()

        if u<=0.5:
            for j in usa_units:
                j.fronty_ale_to_chodzi()
                j.day_gone()
            for j in china_units:
                j.day_gone()
        else:
            for j in china_units:
                j.fronty_ale_to_chodzi()
                j.day_gone()

            for j in usa_units:
                j.day_gone()

        for j in usa_units:
            us_alive_counter += j.alive
        for j in china_units:
            ch_alive_counter += j.alive
        # for j in GraphNodes:
        #     check_battle_parameters(j,usa_units,china_units)

        for j in usa_units:
            for k in china_units:
                battle_units(j, k)

        # print("day " + str(i),
        #     "USA: " + str(us_alive_counter) + "/" + str(len(usa_units)),
        #       "CHINA: " + str(ch_alive_counter) + "/" + str(len(china_units)))

        # if us_alive_counter == 0 or ch_alive_counter == 0:
        #     break
            # print( i, us_alive_counter, ch_alive_counter)

    data = {
        'type': 'FeatureCollection',
        'features': obiekty}

    m = folium.Map(location=[30, 200], zoom_start=4)

    # dodanie danych geograficznych z czasem
    TimestampedGeoJson(data,
                       period='P1D',
                       duration='PT1H',
                       add_last_point=True,
                       auto_play=True,
                       loop=False,
                       max_speed=5,
                       loop_button=True).add_to(m)
    m.save("war_projection.html")

    plt.plot(GDPu, color='blue', label="USA")
    plt.plot(GDPc, color='red', label="China")
    plt.title("PKB")
    plt.xlabel("Dni")
    plt.ylabel("Bln USD")
    plt.legend()
    plt.show()

def main3(usa_unit, china_unit):
    """
    Simulate war (military units movement on map)
    """
    obiekty = []

    for i in range(1000):

        GDPu, GDPc = Economy(peace=False, i=i, usa_uni = usa_unit, china_uni = china_unit)


        if i%50 == 49:
            xd = np.random.random()
            if 0<=xd<1/3:

                usa_units.append(militaryUnit(belong="usa", name=str(int(i/10+13)), numbers=[5000, 10, 50, 15], loc=LosAlamos, destination_list=[LosAlamos,SanDiego,Honolulu,Guam,Philippnes,Hainan,Maoming]))
                china_units.append(militaryUnit(belong="china", name=str(int(i/10+9)), numbers=[15000, 50, 50, 10],loc=SychuanBasin, destination_list=[SychuanBasin,TaihangShan,Pekin,Korea_Polnocna,Korea_Poludniowa,Tokyo]))
            elif 1/3 <= xd < 2/3:
                usa_units.append(militaryUnit(belong="usa", name=str(int(i/10+13)), numbers=[5000, 10, 50, 15], loc=Seattle, destination_list = [Seattle, Honolulu, Kioto, Nagasaki, Okinawa, Tainan, Hsinchu, Fujian, Shanghai]))
                china_units.append(militaryUnit(belong="china", name=str(int(i/10+9)), numbers=[15000, 50, 50, 10], loc=SychuanBasin, destination_list=[SychuanBasin]))
            else:
                usa_units.append(militaryUnit(belong="usa", name=str(int(i/10+13)), numbers=[5000, 10, 50, 15], loc=SanDiego, destination_list=[SanDiego,Honolulu,Tokyo,Korea_Poludniowa,Korea_Polnocna,Pekin,TaihangShan]))
                china_units.append(militaryUnit(belong="china", name=str(int(i/10+9)), numbers=[15000, 50, 50, 10], loc=Maoming, destination_list=[Maoming,Hainan, Philippnes, Guam]))
        for j in usa_units:
            if j.loc==ThreeGorgesDam and j.inTravel==False:
                ThreeGorgesDam.bum=True
                j.alive = False
        
        # u = np.random.random()
        # if u < 0.001:
        #     LosAlamos.trump = True
        #     print('trump')
        #
        # if u > 0.001 and u < 0.003:
        #     Pekin.bingchilling = True
        #     print('bingchilling')
        #
        # if u > 0.005 and u < 0.009:
        #     SychuanBasin.mnich = True
        #     print('mnich')
        #
        # if u > 0.15 and u < 0.17:
        #     Pekin.puchatek = True
        #     print('puchatek')
        #
        # if u < 0.5 and u > 0.499:
        #     Pekin.coronav2 = True
        #     print('coronav2')

        obiekty.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [170, 50]
            },
            'properties': {
                "time": 1.68493 * 10 ** 12 + 86400000 * i,
                'popup': "USA: " + str(GDPu[i]),
                'icon': 'marek', 'iconstyle': {'color': 'blue', 'stroke': 'true', 'fillOpacity': 0.3}
            }
        })
        obiekty.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [160, 50]
            },
            'properties': {
                "time": 1.68493 * 10 ** 12 + 86400000 * i,
                'popup': "Chiny: " + str(GDPc[i]),
                'icon': 'marek', 'iconstyle': {'color': 'red', 'stroke': 'true', 'fillOpacity': 0.3}
            }
        })
        if ThreeGorgesDam.bum==True:
            obiekty.append({
                            'type': 'Feature',
                            'geometry': {
                                'type': 'Point',
                                'coordinates': [ThreeGorgesDam.loc[1], ThreeGorgesDam.loc[0]]
                            },
                            'properties': {
                                "time": 1.68493 * 10 ** 12 + 86400000 * i,
                                'popup': str("Tama bum!!!"),
                                'icon': 'circle', 'iconstyle': {'color': 'green', 'stroke': 'true', 'fillOpacity': 0.3}
                            }
                        })

        for jednostka in usa_units:
            if jednostka.alive == True:
                if jednostka.inFight == True:
                    if (jednostka.loc in Usa360):
                        cord1, cord2 = jednostka.loc.loc[1] + 360, jednostka.loc.loc[0]
                    else:
                        cord1, cord2 = jednostka.loc.loc[1], jednostka.loc.loc[0]
                    obiekty.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [cord1, cord2]
                        },
                        'properties': {
                            "time": 1.68493 * 10 ** 12 + 86400000 * i,
                            'popup': str(jednostka.name),
                            'icon': 'circle', 'iconstyle': {'color': 'black', 'stroke': 'true', 'fillOpacity': 1}
                        }
                    })
                else:
                    if (jednostka.loc in Usa360):
                        cord1, cord2 = jednostka.loc.loc[1] + 360, jednostka.loc.loc[0]
                    else:
                        cord1, cord2 = jednostka.loc.loc[1], jednostka.loc.loc[0]
                    obiekty.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [cord1, cord2]
                        },
                        'properties': {
                            "time": 1.68493*10**12+86400000* i,
                            'popup': str(jednostka),
                            'icon': 'circle', 'iconstyle': {'color': 'blue'}
                        }
                    })
            else:
                continue
        for jednostka in china_units:
            if jednostka.alive == True:
                if jednostka.inFight == True:
                    if (jednostka.loc in Usa360):
                        cord1, cord2 = jednostka.loc.loc[1] + 360, jednostka.loc.loc[0]
                    else:
                        cord1, cord2 = jednostka.loc.loc[1], jednostka.loc.loc[0]
                    obiekty.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [cord1, cord2]
                        },
                        'properties': {
                            "time": 1.68493 * 10 ** 12 + 86400000 * i,
                            'popup': str(jednostka.name),
                            'icon': 'circle', 'iconstyle': {'color': 'black', 'stroke': 'true', 'fillOpacity': 1}
                        }
                    })
                else:
                    if (jednostka.loc in Usa360):
                        cord1, cord2 = jednostka.loc.loc[1] + 360, jednostka.loc.loc[0]
                    else:
                        cord1, cord2 = jednostka.loc.loc[1], jednostka.loc.loc[0]
                    obiekty.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [cord1, cord2]
                        },
                        'properties': {
                            "time": 1.68493*10**12+86400000* i,
                            'popup': str(jednostka),
                            'icon': 'circle', 'iconstyle': {'color': 'red'}
                        }
                    })
            else:
                continue

        us_alive_counter, ch_alive_counter = 0, 0
        u=random.random()

        if u<=0.5:
            for j in usa_units:
                j.fronty_ale_to_chodzi2()
                j.day_gone()
            for j in china_units:
                j.day_gone()
        else:
            for j in china_units:
                j.fronty_ale_to_chodzi2()
                j.day_gone()

            for j in usa_units:
                j.day_gone()

        for j in usa_units:
            us_alive_counter += j.alive
        for j in china_units:
            ch_alive_counter += j.alive
        for j in GraphNodes:
            check_battle_parameters(j,usa_units,china_units)


        # print("day " + str(i),
        #     "USA: " + str(us_alive_counter) + "/" + str(len(usa_units)),
        #       "CHINA: " + str(ch_alive_counter) + "/" + str(len(china_units)))

        # if us_alive_counter == 0 or ch_alive_counter == 0:
        #     break
            #print( i, us_alive_counter, ch_alive_counter)


    data = {
        'type': 'FeatureCollection',
        'features': obiekty}

    m = folium.Map(location=[30, 200], zoom_start=4)

    # dodanie danych geograficznych z czasem
    TimestampedGeoJson(data,
                       period='P1D',
                       duration='PT1H',
                       add_last_point=True,
                       auto_play=True,
                       loop=False,
                       max_speed=5,
                       loop_button=True).add_to(m)
    m.save("elson2.html")

    plt.plot(GDPu, color='blue',label="USA")
    plt.plot(GDPc, color='red',label="China")
    plt.title("PKB")
    plt.xlabel("Dni")
    plt.ylabel("Bln USD")
    plt.legend()
    plt.show()

main2(usa_units,china_units)
#main3(usa_units,china_units)

### all war management end ###
