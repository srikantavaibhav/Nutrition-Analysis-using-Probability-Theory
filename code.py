import math
import matplotlib.pyplot as plt

def dispProbMenu(file):
	print("MENU (in detail)".center(94,"-")+"\n"+file.read()+"-"*94)
	print("The restaurant has 50 items (100g each) in its menu.")
	n=int(input("How many items did the customer order? "))
	ch=int(input("\nProbability Distribution of\n1: Calorie-rich(>300cal) items\n2: Protein-rich(>8%) items\n3: Fat-rich(>15%) items\n4: Carbs-rich(>30%) items\nSelect the probability distribution you require: "))
	while ch not in [1,2,3,4]: ch=int(input("Invalid selection!\nRe-enter valid choice: "))	
	file.close()
	return [n,ch]

def findDistribution(file,n,ch):
	items=[]; val=[]; richItems=[]; richVal=[]; px=[]; threshold=[300,8,15,30]; firstLine=True
	while 1:
		line=file.readline()
		if firstLine: 
			firstLine=False; continue
		if not line: break
		words=list(filter(lambda x: x!='',line.split("\t")))
		items.append(words[1])
		val.append(words[ch+1])
		if float(words[ch+1])>=threshold[ch-1]:
			richItems.append(words[1])
			richVal.append(words[ch+1])
	items.pop(0); val.pop(0)
	s=C(50,n) #|sample space|
	nrich=len(richVal)
	for i in range(0,n+1):
		px.append(C(nrich,i)*C(50-nrich,n-i)/s)
	print("\nFood items with high "+(["Calories","Proteins","Fat","Carbs"][ch-1])+":")
	for i in range(0,nrich):
		print(str(i+1)+".",richItems[i],"("+richVal[i],end='')
		if ch==1: print("cal)")
		else: print("%)")
	print("\nLet X be the number of "+(["Calorie","Protein","Fat","Carbs"][ch-1])+"-rich items in the customer's order.\n"+"Probabilty Distribution Table:")
	print("-"*(9*n+19),"\n|"+"X".center(8)+"|",end='')
	for i in range(0,n+1): print(str(i).center(8)+"|",end='')
	print("\n"+"-"*(9*n+19),"\n|"+"P(X)".center(8)+"|",end='')
	for i in px: print("{0:0.4f}".format(i).center(8)+"|",end='')
	print("\n"+"-"*(9*n+19))
	file.close()
	return px

def findSD(n,px,ch):
	mean,var,sd=0,0,0
	for x in range(0,n+1): mean=mean+x*px[x]
	for x in range(0,n+1): var=var+pow(x-mean,2)*px[x]
	sd=math.sqrt(var)
	print("Mean = {:0.4f}, is the expected average of the number of items with high ".format(mean)+(["Calorie","Protein","Fat","Carbs"][ch-1])+" in the customer's order.\n"+"Variance = {:0.4f}\nStandard Deviation = {:0.4f}".format(var,sd))

def C(n,r):
	f = math.factorial
	return f(n) / (f(r)*f(n-r))

def plot(n,px):
	f=[]; 
	for i in range(n+1):
		sum=0
		for j in range(i+1):
			sum+=px[j]
		f.append(sum)
	plt.bar([i for i in range(n+1)],f,label="F(X)")
	plt.legend()
	plt.xlabel('X')
	plt.ylabel('P(X)')
	plt.title('Cumulative Graph')
	plt.show()
# Driver Code
l=dispProbMenu(open("data.txt"))
px=findDistribution(open("data.txt"),l[0],l[1])
findSD(l[0],px,l[1])
plot(l[0],px)
