from enum import Enum
import random
import time
class Suite(Enum):
    """花色（枚舉）"""
    JOKER,SPADE,HEART,CLUB,DIAMOND=range(5)

class Card:
    """牌"""

    def __init__(self, suite, face):
        self.suite = suite
        self.face = face

    def __repr__(self):
        suites = '🃟♠♥♣♦'
        faces = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return f'{suites[self.suite.value]}{faces[self.face]}'
    
    def __lt__(self, other):
        if self.suite == other.suite:
            return self.face < other.face   # 花色相同比较点数的大小
        return self.suite.value < other.suite.value   # 花色不同比较花色对应的值
    def __eq__(self, other):
        return self.face == other.face
        
    
        
    
class Poker:
    
    """扑克"""

    def __init__(self):
        self.cards = [Card(suite, face)
                      for suite in [Suite(i) for i in range(1,5)]
                      for face in range(1, 14)]  # 52张牌构成的列表
        self.current = 0  # 记录发牌位置的属性

    def shuffle(self):
        """洗牌"""
        self.current = 0
        random.shuffle(self.cards)  # 通过random模块的shuffle函数实现随机乱序

    def deal(self):
        """发牌"""
        card = self.cards[self.current]
        self.current += 1
        return card

    @property
    def has_next(self):
        """还有没有牌可以发"""
        return self.current < len(self.cards)
class Player:
    """玩家"""
    def __init__(self, name):
        self.name = name
        self.cards = []   # 玩家手上的牌
        self.collects=[]  #玩家收回的牌
        self.count=0    #計算收回的牌數
        
    def get_one(self, card):
        """摸牌"""
        self.cards.append(card)

    def draw_one(self):
        """抽牌"""
        return self.cards.pop()
    def is_shuffle(self,ans):
        """是否洗牌"""
        if ans==1:
            random.shuffle(self.cards)
        else:
            pass


    def collect_cards(self, desk_cards):#玩家手中收回的牌
        """收牌"""
        self.collects=self.collects+desk_cards
        return len(self.collects)       #返回玩家收回的牌的總數量
    
    def compare_number(self, other): #與對方玩家比對收回的總牌數,返回較大者
        if self.count >= other.count:
            return self
        else: 
            return other
def main():       
    poker = Poker()
    poker.shuffle()
    while True:
        try:
            player_num=int(input("請輸入2-4的數字，選擇接龍人數："))
            if player_num>4 or player_num<2:
                raise Exception("玩家不能少於2人或多於5人")
        except ValueError as e:
            print ("異常提示：請輸入一個有效數字")
        except Exception as e:
            print(f'異常提示：{e}')
        else:
            break
            
    
    player_name=input("請登錄玩家用戶名：")
    players = [Player(player_name)]
    for j in range(1,player_num):
        players.append(Player(f'虛擬玩家{j}號'))   #分配虛擬玩家，此處也可以鏈接數據庫取得登錄網站的其他用戶玩家
    desk_cards=[Card(Suite.JOKER,0)]
    # 将牌轮流发到每个玩家手上
    for _ in range(52//player_num):
        for player in players:
            player.get_one(poker.deal())

   
    while True:        
        for player in players:
            ans=0
            if player==players[0]:
                answer=input("shuffle?yes or no ?please answer with y or n or any key:")
                if answer=='y':
                    ans=1
                else:
                    pass
            player.is_shuffle(ans)
            temp=player.draw_one()

            print(f'{player.name}抽出一張牌{temp}')
        
            if temp.face not in list(map(lambda x: x.face, desk_cards)):
                desk_cards.append(temp)
            
            else:
                desk_cards.append(temp)
                n=desk_cards.index(temp)
                player.count=player.collect_cards(desk_cards[n:])
                cards_len=len(desk_cards[n:])
                desk_cards=desk_cards[:n]
                print(f'碰！{player.name}收回{cards_len}張牌,手中收回的已有的牌數{player.count}張')
            print(f'桌面上的牌：{desk_cards}')
            time.sleep(1)
        if not player.cards:
            print("玩家手中都沒牌了，開始計數")
            break
    winner=players[0]
    for i in range(1,len(players)):
        winner=winner.compare_number(players[i])
    collect_nums=[player.count for player in players]
    indices=[index for index,value in enumerate(collect_nums) if value == winner.count]

    if len(indices)!=len(players):
        print("勝者是：")
        for index in indices:
            print(players[index].name,end=" ")
    else:
        print("平局")
if __name__=="__main__":
    main()