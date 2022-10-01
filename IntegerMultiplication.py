import sys
import math
import time
from random import randint
import matplotlib.pyplot as plt
import random
import numpy as np

def AddBigInt(x,y):
    x=str(x)
    y=str(y)
    x=x[::-1]
    y=y[::-1]
    smaller=len(x)
    greater_x=False
    if ( len(x) > len(y) ):
        greater= len(x)
        greater_x = True
        smaller= len(y)
    else: 
        greater=len(y)
        smaller = len(x)
    
    result=[0]*(greater + 1)
    index=0
    carry=0
    for i in range(smaller):
        n1=int(x[i])
        n2=int(y[i])
        sum=n1+n2+carry
        carry= sum // 10
        result[index] = sum % 10
        index+=1
    if (greater_x):
        for i in range(index,greater):
            sum=carry+ int(x[i])
            result[index]=sum % 10
            carry = sum //10
            index+=1
    else:
        for i in range(index,greater):
            sum=carry+ int(y[i])
            result[index]=sum % 10
            carry = sum //10
            index+=1
    if (carry!=0):
        result[index]=carry
    final_result = ""
    i = len(result) - 1
    while (i >= 0 and result[i] == 0): 
        i -= 1
    if (i == -1): 
        return "0"
    final_result = "" 
    while (i >= 0): 
        final_result += str(result[i] ) 
        i -= 1
    
    return final_result

def smaller(x,y):
    if ( len(x) < len(y) ):
        return True
    elif ( len(y) < len(x) ):
        return False
    
    
    for i in range(len(x)):
        if (x[i] < y[i] ):
            return True
        elif (x[i] > y[i]):
            return False

    return False

def SubtractBigInt(x,y):
    x=str(x)
    y=str(y)
    #check which is smaller
    #ensure that x is smaller
    if (smaller (x,y)):
        pass
    else:
        #y is smaller 
        temp=x
        x=y
        y=temp

    smaller_length=len(x)
    greater_length=len(y)
    x=x[::-1]
    y=y[::-1]
    carry=0
    result=""

    for i in range(smaller_length): 
        diff= int(y[i]) - int(x[i]) - carry
        if  (diff < 0):
            #diff=temp - int(x[i])
            diff=diff+10
            carry=1
        else:
            carry=0
        
        result=result+str(diff)

    for i in range(smaller_length, greater_length):
        diff = (int(y[i]) - carry)
        if (diff < 0):
            diff += 10
            carry = 1
        else:
            carry = 0
        result = result+str(diff)

    result=result[::-1]
    j=0
    while ( j< len(result) and result[j] == '0'):
        j += 1

    if (j == len(result)): 
        return "0"

    final_result = "" 
    while (j < len(result)): 
        final_result+= str(result[j] )
        j += 1

    return final_result

def DAC(num1,num2):
    #Karatsuba Algorithm
    if (num1 =="" or num2==""):
        return '0'
    if (len(str(num1))==1 or len(str(num2))==1):
        return int(num1)*int(num2)

    else:
        str_num1=str(num1)
        str_num2=str(num2)
        j=max(len(str_num1),len(str_num2))
        
        half=j//2
        minus_m=half * -1

        a = str_num1[:minus_m]
        b = str_num1[minus_m:]
        c = str_num2[:minus_m]
        d = str_num2[minus_m:]

        e = DAC( a , c )
        f = DAC( b , d )
        g = DAC(AddBigInt(a,b),AddBigInt(c,d))
        A = AddZeroesAhead ( str(e) , (2*half))
        B = SubtractBigInt ( SubtractBigInt(g,f), e)
        B = AddZeroesAhead (str(B), half)
        prod = AddBigInt ( AddBigInt (A,B) , f)

        #prod = e * ( 10**(2*half) ) + ( (g - e -f ) * (10**half) ) + f
        return prod


def AddZeroesAhead(a,num_zeroes):
    x= num_zeroes + len(a)
    res = a.ljust(x, '0')
    return res

def BruteForce(x,y):
    len1=len(x)
    len2=len(y)
    if ( len1 ==0 or len2 == 0):
        return "0"
    
    result=[0] * (len1 + len2)
    index1=0
    index2=0
    
    start = time.time()
    for i in reversed(range(len1)):
        n1= int (x[i])
        index2 = 0
        carry = 0

        for j in reversed(range(len2)):
            n2 = int(y[j])
            prod = n1 * n2 + result[ index1 + index2 ] + carry
            carry = prod // 10
            result [ index2 + index1 ] = prod % 10
            index2 += 1

        if (carry > 0):
            result [index2 + index1] = carry + result [index1 + index2] #ensuring that last iteration's carry is added

        index1 += 1 # for shifting to left


    end = time.time()

    difference = (end-start) * 1000
    final_result = ""
    i = len(result) - 1
    while (i >= 0 and result[i] == 0): 
        i -= 1

    if (i == -1): 
        return "0"

    final_result = "" 
    while (i >= 0): 
        final_result += str(result[i] ) 
        i -= 1
    return final_result, difference

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def MakePlots():
    digits=[1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
    timesforB=[]
    timesforD=[]
    for i in digits:
        x=random_with_N_digits(i)
        y=random_with_N_digits(i)
        ans,t = BruteForce (str(x),str(y))
        print("B-force: ",t)
        timesforB.append(t)

        start=time.time()
        j=DAC(str(x),str(y))
        end=time.time()
        time_taken=(end-start) * 1000
        print("DAC: ",time_taken)
        timesforD.append(time_taken)

    plt.plot(digits, timesforB, '-b', label = 'Brute Force')
    plt.xlabel('Input Size')
    plt.ylabel('Runtime in milliseconds')
    plt.title('Algorithm Runtime')
    plt.plot(digits, timesforD,'-r', label = 'Divide and Conquer')
    plt.legend(framealpha = 1, frameon = True)
    plt.show()





def main():

    #MakePlots()
    print("To generate the plot, please uncomment the MakePlots() command in main(). My Karatsuba algorithm is taking more time initially because I implemented BigInt manually. Divide and conquer is increasing at a decreasing rate. So Brute Force will eventually take over.  ")
    ask=input("Please tell which algorithm to run?: ")
    num1=input("Enter integer 1: ")
    num2=input("Enter integer 2: ")
    if (ask=="B" or ask=="b"):
        ans, timetaken = BruteForce(str(num1), str(num2))
        print(str(ans))
        print("Time taken for brute force:\n" + str(timetaken))
        print("\n")
    
    elif (ask=="D" or ask=="d"):
        start = time.time()
        ans = DAC(str(num1),str(num2))
        end = time.time()
        diff = end - start
        print(str(ans))
        print("Time taken for Karatsuba Algorithm:\n" + str(diff))
        print("\n")



if __name__ == "__main__":
    main()
