print("Hi, I'm the diagnoser! Please answer the following 14 questions to receive a diagnosis for your illness.                                                                                                                                                         ")

a = "fever"
b = "cough"
c = "shortness of breath"
d = "fatigue"
e = "loss of taste/smell/apetite"
f = "diarreha"
g = "abdominal cramps"
h = "nausea"
i = "vomiting"
j = "pain when swallowing"
k = "tonsils pain"
l = "sore throat"
m = "angry outbursts"
n = "no motivation, apathy"
o = "trouble sleeping"


symptoms = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o]

correctsymp = []
correct_symp_idx = 0
for index in range(len(symptoms)):
  curr_sym = symptoms[index]
  print("Do you have a " + curr_sym + ", yes or no? ")
  
  response = input()
  if response == "yes":
   correctsymp.insert(correct_symp_idx, curr_sym)
   correct_symp_idx += 1
   
#print(correctsymp)

covid_symp_counter = 0


for index in range(len(correctsymp)):
  if correctsymp[index] == a or correctsymp[index] == b or correctsymp[index] == c or correctsymp[index] == d or correctsymp[index] == e:
    covid_symp_counter = covid_symp_counter + 1
#print(covid_symp_counter)
    

flu_symp_counter = 0

for index in range(len(correctsymp)):
  if correctsymp[index] == f or correctsymp[index] == g or correctsymp[index] == h or correctsymp[index] == i:
    flu_symp_counter = flu_symp_counter + 1
#print(flu_symp_counter)


strep_symp_counter = 0

for index in range(len(correctsymp)):
  if correctsymp[index] == j or correctsymp[index] == k or correctsymp[index] == l:
    strep_symp_counter = strep_symp_counter + 1
#print(strep_symp_counter)

depression_symp_counter = 0

for index in range(len(correctsymp)):
  if correctsymp[index] == m or correctsymp[index] == n or correctsymp[index] == o:
    depression_symp_counter = depression_symp_counter + 1
#print(depression_symp_counter)

if len(correctsymp) == 0:
  print("you do not have any illnesses!")

  

diagnoser_list = [covid_symp_counter, flu_symp_counter, strep_symp_counter, depression_symp_counter]
diagnoser_max = 0

#print(diagnoser_list)

for index in range (len(diagnoser_list)):
  if (diagnoser_max < diagnoser_list[index]) :
    diagnoser_max = diagnoser_list[index]

#print(diagnoser_max)

if diagnoser_max == covid_symp_counter:
    print("You might have COVID-19")
    print("Quarantine in your home and do not see other people. ")

if diagnoser_max == flu_symp_counter:
    print("You might have the stomach flu")
    print("Take some Tylenol and drink hot water. If you do not completely heal in 1 week, seek help from a doctor.")

if diagnoser_max == strep_symp_counter:
    print("You might have strep throat")
    print("Drink lots of hot water and gargle salt water. If it does not heal in 3 days, consult a doctor.")

if diagnoser_max == depression_symp_counter:
    print("You might have depression")
    print("Go see a therapist for help.")