from time import time
import matplotlib.pyplot as plt 

C_matched={} #candidates who r matched are in this dict.
SlotsOfAllH={}  #a dict which contains the slots of each hospital
PrefListH={}  #contains the pref list of each hospital
PrefListC={} #this contains the candidate's hos[ital ranks
TotalSlotsAvailable=0
NumC=0
NumH=0
def parse(filename):
    global NumC
    global NumH
    global PrefListH
    global PrefListC
    global TotalSlotsAvailable
    global C_matched
    global SlotsOfAllH
    C_matched.clear() #candidates who r matched are in this dict.
    SlotsOfAllH.clear()  #a dict which contains the slots of each hospital
    PrefListH.clear()  #contains the pref list of each hospital
    PrefListC.clear() #this contains the candidate's hos[ital ranks

    with open(filename, "r") as file: 
        data = file.readlines() 
        line_1=data[0].split()
        NumH=int(line_1[0])
        NumC=int(line_1[1])
        line_2=data[1].split()
        for i in range(NumH):
            SlotsOfAllH[i]=int (line_2[i])
        
        start=2
        end=2+NumH

        for i in range(start,end):
            line=data[i]
            TheList=[]
            for k in line.split():
                TheList.append(int(k))
            PrefListH[i-start]=TheList
        
        start=2+NumH
        end=start+NumC

        for i in range(start,end):
            line=data[i]
            TheList=[]
            for k in line.split():
                TheList.append(int(k))
        
            PrefListC[i-start]=TheList

        for i in PrefListC.keys():
            TheList=PrefListC[i]
            Rank=[None] * len(TheList)
            for k in range(len(TheList)):
                Rank[TheList[k]]=k
            PrefListC[i]=Rank

        for i in range(len(SlotsOfAllH)):
            TotalSlotsAvailable=TotalSlotsAvailable+SlotsOfAllH[i]    
    
def MakeMatches():
    global NumC
    global NumH
    global PrefListH
    global PrefListC
    global TotalSlotsAvailable
    global C_matched
    global SlotsOfAllH

    hosp=0
    while ( TotalSlotsAvailable!=0 ): 

        slots=SlotsOfAllH[hosp] 
        if (slots!=0):
            candidate=PrefListH[hosp].pop(0) #highest ranked candidate in hosp's list. this is str
            if (candidate not in C_matched.keys()): #Candidate is free
                C_matched[candidate]=hosp #Candidate gets matched with the proposing hospital
                slots=slots-1
                SlotsOfAllH[hosp]=slots
                TotalSlotsAvailable=TotalSlotsAvailable-1
            else:#was paired with someone else
                H_=C_matched[candidate] #the hospital with which the candidate is matched already.
                if ( PrefListC[candidate][H_] < PrefListC[candidate][hosp] ):
                    pass
                else:
                    SlotsOfH_=SlotsOfAllH [ H_ ] + 1  #since H' slot got free
                    SlotsOfAllH [ H_ ] = SlotsOfH_ 
                    C_matched[candidate]=hosp #Candidate gets matched with the proposing hospital
                    slots=slots-1
                    SlotsOfAllH[hosp]=slots    

        hosp=(hosp+1) % NumH

def Output(filename):
    global C_matched
    global NumC
    output=[None] * NumC
    for i in range(NumC):
        output[i]=-1
    for i in C_matched.keys():
        output[i]=C_matched[i]
    
    Content=str(output[0])
    for i in range(1,len(output)):
        Content=Content+' '+str(output[i])
    
    writeTo=filename.split('.')[0] + '.out'
    f=open(writeTo,"w")
    f.write( Content )
    f.close()

def main():


    #code for measuring time.

    # fileNameList=['1-5-5.in','1-10-5.in','3-3-3.in','3-10-3.in','40.in','80.in','160.in','320.in']
    # TimeList=[]
    # for i in fileNameList:
    #     TotalTime=0
    #     for k in range(10):
    #         parse(i)
    #         start=time()
    #         MakeMatches()
    #         end=time()
    #         difference=(end-start)*1000
    #         TotalTime=TotalTime+difference
    #     TimeList.append(TotalTime/10)
        
    # NumOfH=[1,1,3,3,40,80,160,320]
    # plt.plot(NumOfH,TimeList,'*-')
    # plt.xlabel('Number of hospitals')
    # plt.ylabel('Time elapsed (ms)')
    # plt.show()    

    filename=input("Please enter the file's name: ")
    parse(filename)
    MakeMatches()
    Output(filename)


if __name__=="__main__":
    main()


      

