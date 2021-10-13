import matplotlib.pyplot as plt
days=[1,2,3,4,5]
sleeping=[7,8,9,6,5]
eating=[4,5,7,8,5]
working=[4,5,6,1,2]
playing=[4,7,8,5,2]

plt.plot([],[],label="sleeping",linewidth=5,color='r')
plt.plot([],[],label="eating",linewidth=5,color='b')
plt.plot([],[],label="working",linewidth=5,color='g')
plt.plot([],[],label="playing",linewidth=5,color='k')
plt.stackplot(days,sleeping,eating,working,playing,colors=['r','b','g','k'])
plt.xlabel('dfkidgh')
plt.legend()
plt.show()
