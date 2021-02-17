import numpy as np
import matplotlib.pyplot as plt
import pickle
import time

def CheckCondition(state,condition):
	if (np.sum(np.multiply(state, condition))-np.sum(np.multiply(condition, condition)))==0:
		return True
	else:
		return False


def CheckVisited(state,vertices):
	for i in range(len(vertices)):
		if np.linalg.norm(np.subtract(state,vertices[i]))==0:
			return True
	return False


def ComputeNextState(state, effect):
	newstate=np.add(state, effect)
	return newstate


Predicates=['InHallway', 'InKitchen', 'InOffice', 'InLivingRoom', 'InGarden','InPantry','Chopped','OnRobot']

Objects=['Robot','Strawberry','Lemon', 'Paper', 'Knife'] 

nrPredicates=len(Predicates)
nrObjects=len(Objects)

ActionPre=[]
ActionEff=[]
ActionDesc=[]

###Move to hallway
for i in range(1,5,1):
	Precond=np.zeros([nrObjects, nrPredicates])
	Precond[0][0]=-1 #Robot not in hallway
	Precond[0][i]=1  #Robot in i-th room

	Effect=np.zeros([nrObjects, nrPredicates])
	Effect[0][0]=2.  #Robot in the hallway
	Effect[0][i]=-2. #Robot not in the i-th room

	ActionPre.append(Precond)
	ActionEff.append(Effect)
	ActionDesc.append("Move to InHallway from "+Predicates[i])

###Move to room
for i in range(1,5,1):
	Precond=np.zeros([nrObjects, nrPredicates])
	Precond[0][0]=1  #Robot in the hallway
	Precond[0][i]=-1 #Robot not in the ith room

	Effect=np.zeros([nrObjects, nrPredicates])
	Effect[0][0]=-2. #Robot not in the hallway
	Effect[0][i]=2.  #Robot in the ith room

	ActionPre.append(Precond)
	ActionEff.append(Effect)
	ActionDesc.append("Move to "+Predicates[i]+" from InHallway")

###ADD YOUR CODE HERE FOR THE 3 ADDITIONAL ACTIONS:

## Actions to be added:
## 1) Move to pantry from kitchen
Precond = np.zeros([nrObjects, nrPredicates])
Precond[0][1] = 1 # robot in kitchen
Precond[0][5] = -1 # robot not in pantry

Effect = np.zeros([nrObjects, nrPredicates])
Effect[0][1] = -2 # robot not in the kitchen
Effect[0][5] = 2 # robot in pantry

ActionPre.append(Precond)
ActionEff.append(Effect)
ActionDesc.append("Move to " + Predicates[5] + " from InKitchen")

 
## 2) Move to kitchen from pantry
Precond = np.zeros([nrObjects, nrPredicates])
Precond[0][5] = -2. # robot not in pantry
Precond[0][2] = 2 # robot in kitchen

ActionPre.append(Precond)
ActionEff.append(Effect)
ActionDesc.append("Move to InKitchen from InPantry")
 

## 3) Cut fruit
for i in range (1, 5, 1):
	Precond = np.zeros([nrObjects, nrPredicates])
	Precond[0][i] = -1 # robot not in the ith room
	Precond[0][i] = 1 # robot in the kitchen
	Precond[4][1] = 1 # knife in the kitchen

	for j in range (1,2,1): # go through fruits
		Precond[j][1] = 1 # fruit in the kitchen
		Precond[j][6] = -1 # fruit is not chopped

		Effect = np.zeros([nrObjects, nrPredicates])
		Effect[j][6] = 2. # Fruit is chopped
		ActionPre.append(Precond)
		ActionEff.append(Effect)
		ActionDesc.append(f'Fruit {Objects[j]} is chopped InKitchen.')





###Pickup object
for i in range(1,6,1):
	for j in range(1,5,1):
		Precond=np.zeros([nrObjects, nrPredicates])
		Precond[0][i]=1 #Robot in ith room
		Precond[j][i]=1 #Object j in ith room
		Precond[j][-1]=-1 #Object j not on robot

		Effect=np.zeros([nrObjects, nrPredicates])
		Effect[j][i]=-2 #Object j not in ith room
		Effect[j][-1]=2 # Object j on robot

		ActionPre.append(Precond)
		ActionEff.append(Effect)
		ActionDesc.append("Pick up "+Objects[j]+" from "+Predicates[i])
	

###Place object
for i in range(1,6,1):
	for j in range(1,5,1):
		Precond=np.zeros([nrObjects, nrPredicates])
		Precond[0][i]=1 #Robot in ith room
		Precond[j][i]=-1 #Object j not in ith room
		Precond[j][-1]=1 #Object j on robot

		Effect=np.zeros([nrObjects, nrPredicates])
		Effect[j][i]=2.  #Object j in ith room
		Effect[j][-1]=-2 #Object j not on robot

		ActionPre.append(Precond)
		ActionEff.append(Effect)
		ActionDesc.append("Place "+Objects[j]+" at "+Predicates[i])


InitialState=-1*np.ones([nrObjects, nrPredicates])
InitialState[0][0]=1 # Robot is in the hallway
InitialState[1][4]=1 # Strawberry is in the garden
InitialState[2][5]=1 # Lemon is in the pantry
InitialState[3][2]=1 # Paper is in the office
InitialState[4][2]=1 # Knife is in the office

GoalState=np.zeros([nrObjects, nrPredicates])
GoalState[0][1]=1 # Robot is in the kitchen
GoalState[1][1]=1 # Strawberry is in the kitchen
GoalState[2][4]=1 # Lemon is in the Garden
GoalState[1][6]=1 # Strawberry is chopped


np.random.seed(13)


# Search for Solution
vertices=[]
parent=[]
action=[]

cost2come=[]

Queue=[]
Queue.append(0)
vertices.append(InitialState)
parent.append(0)
action.append(-1)
cost2come.append(0)

FoundPath=False

### Add your code here to generate path ###
while len(Queue) > 0:
	# highest priority
	P = np.array([cost2come[q] for q in Queue])
	id = P.argmin() # select min cost2come node to expand

	x = Queue[id]
	del Queue[id]

	if CheckCondition(vertices[x], GoalState): # check goal
		FountPath=True
		print("\n FoundPath: ",FoundPath)
		break

	for i, action_pre in enumerate(ActionPre): # check each action precond + visited
		state = vertices[x]
		action_eff = ActionEff[i]
		if CheckCondition(state,action_pre):
			if not CheckVisited(ComputeNextState(state,action_eff), vertices):
				#add node to graph and queue
				vertices.append(ComputeNextState(state,action_eff))
				action.append(i)
				parent.append(x)
				cost2come.append(cost2come[x]+1)
				Queue.append(len(vertices)-1)


# Once you've found a path, use the code below to print out your plan
print(f"FoundPath: {FoundPath}")

Plan=[]
if FoundPath:
	while not x==0:
		Plan.insert(0,action[x])
		x=parent[x]
		
for i in range(len(Plan)):
	print(ActionDesc[Plan[i]])
			

