import threading
import time
import random
import string

class TommyCat:
    def __init__(self,dataFile):       #初始化函数 

        self.dataFile = dataFile       #self的存档
        self.extractData()             #从存档中载入猫的信息       
        self.fun_timer()               #启动定时器
        self.run = 1                   #bye时值变为0，退出循环

    def extractData(self):             #加载存档函数
        try:                           #尝试该存档是否存在
            trydata = open(self.dataFile,"r")
            trydata.close()
            
        except IOError:                 #如果存档不存在则进入错误处理阶段
            trydata=open(self.dataFile,"w")  #创建新存档并初始化数据
            trydata.write(str(random.randint(0,23)))
            trydata.write("\n")
            trydata.write(str(random.randint(0,100)))
            trydata.write("\n")
            trydata.write(str(random.randint(0,100)))
            trydata.write("\n")
            trydata.write(str(random.randint(0,100)))
            trydata.close()
        
        data = open(self.dataFile,"r")  #载入猫的存档
        status = data.read().splitlines()
        self.hours = int (status[0])
        self.hungry = int (status[1])
        self.happiness = int (status[2])
        self.health = int (status[3])
        data.close()
        self.setStatus()

    def setStatus(self):                   #通过时间设定状态
        if 0<=self.hours<=7:
            self.statusNow = "我在睡觉......"
            self.wake_sleep = "sleep"
        else:
            self.statusNow = "我醒着但很无聊......"
            self.wake_sleep = "wake"

    def printStatus(self):                 #打印状态
        print("当前时间: %2d点"%self.hours)
        print("我当前的状态： ",self.statusNow)
        print("Happiness:   Sad","*"*(self.happiness//2)+"_"*(50-self.happiness//2),"Happy(%03d)"%self.happiness)
        print("Hungry:     Full","*"*(self.hungry//2)+"_"*(50-self.hungry//2),"Hungry(%03d)"%self.hungry)
        print("Health:     Sick","*"*(self.health//2)+"_"*(50-self.health//2),"Healthy(%03d)"%self.health)

    def fun_timer(self):                #定时器函数，不清楚原理，会用就行
        self.hours+=1                   #self的时间在这个类中相当于全局变量，但是前面必须加self
        self.changeIndex()
        if self.hours > 23:
            self.hours = 0

        self.timer = threading.Timer(5.0,self.fun_timer)
        self.timer.start()

    def changeIndex(self):
        #if 0<= self.hours <=7:             只有在letalone状态才能这样，不然持续之前的状态
            #self.wake_sleep = 'sleep'
        #else:
            #self.wake_sleep = 'wake'

        if self.wake_sleep == "wake" and self.hours == 24:#到了0点，如果是letalone状态，即0点之前是wake，则自动转为sleep
            self.wake_sleep = "sleep"
        
        if self.wake_sleep == "sleep" and self.hours == 8:
            self.wake_sleep = "wake"

        if self.statusNow == "我醒着但很无聊......":
            self.hungry += 2
            self.happiness -= 1
        elif self.statusNow == "我在睡觉......":
            self.hungry += 1
        elif self.statusNow == "我在散步......":
            self.hungry += 3
            self.health += 1
        elif self.statusNow == "我在玩耍......":
            self.hungry += 3
            self.happiness += 1
        elif self.statusNow == "我在吃饭......":
            self.hungry -= 3
        elif self.statusNow == "我在看医生......":
            self.health += 4

        if self.hungry > 80 or self.hungry < 20:
            self.health -= 2
        if self.happiness < 20:
            self.health -= 1
        if self.hungry >= 100:self.hungry = 100
        if self.hungry <= 0:self.hungry = 0
        if self.happiness >= 100:self.happiness = 100
        if self.happiness <= 0:self.happiness = 0
        if self.health >= 100:self.health = 100
        if self.health <= 0:self.health = 0        

    def changeStatus(self,command):
        if command == "walk":
            self.statusNow = "我在散步......"
        elif command == "play":
            self.statusNow = "我在玩耍......"
        elif command == "feed":
            self.statusNow = "我在吃饭......"
        elif command == "seedoctor":
            self.statusNow = "我在看医生......"
        elif command == "letalone":
            self.setStatus()
        else:
            print("我不懂你在说什么")
        print (self.statusNow)


    def save(self):                     #保存
        data = open(self.dataFile,"w")
        data.write(str(self.hours))
        data.write("\n")
        data.write(str(self.hungry))
        data.write("\n")
        data.write(str(self.happiness))
        data.write("\n")
        data.write(str(self.health))
        data.close()

    def solveCommand(self,command):
        if command == "bye":
            print("记得来找我!Bye.....")
            self.timer.cancel()
            self.save()
            self.run = 0
        elif command == "status":
            self.printStatus()
        elif self.wake_sleep == "sleep" and (command == "walk" or command == "play" or command == "feed" or command == "seedoctor"):
            yes_no = input("你确认要吵醒我吗？我在睡觉，你要是坚持吵醒我，我会不高兴的！(y表示是/其他表示不是)")
            if yes_no == "y":
                self.happiness -= 4
                self.changeStatus(command)
            else: 
                statusnow = "我在睡觉......"
                print(self.statusNow)
        else:
            self.changeStatus(command)

    def printTitle(self):
        print("我的名字叫Tommy,一只可爱的猫咪....")
        print("你可以和我一起散步，玩耍，你也需要给我好吃的东西，带我去看病，也可以让我发呆.....")
        print("Commands:")
        print("1.walk:散步")
        print("2.play:玩耍")
        print("3.feed:喂我")
        print("4.seedoctor:看医生")
        print("5.letalone:让我独自一人")
        print("6.status:查看我的状态")
        print("7.bye:不想看到我")
        print()
        print()

    def startProject(self):
        self.printTitle()
        self.printStatus()
        while self.run:
            print()
            command = input("你想： ")
            self.solveCommand(command)

def startGame():
    myCat = TommyCat("mycat.txt")
    myCat.startProject()

if __name__== '__main__':
    startGame()

