import matplotlib.pyplot as plt
from statistics import mean
import typingauto

typingauto.startcount()

averages = []
dates = []

lst = typingauto.getspeed()
avg = int(mean(lst))

with open("averages.txt", "r") as reader:
    avgs = (reader.readline()).split(" ")
    dates = (reader.readline()).split()
    for i in avgs:
        try:
            averages.append(int(i.strip()))
        except:
            pass



averages.append(avg)



datetoadd = typingauto.getdate()
dates.append(datetoadd)

empdate = ''

for j in range(0, len(dates)):
    if dates[j] == empdate:
        dates.remove(empdate)
    else:
        pass


with open("averages.txt", "w+") as writer:
    for i in averages:
        writer.write(str(i) + " ")
    writer.write("\n")
    for i in dates:
        writer.write(i.strip() + " ")


x1 = dates
y1 = averages

x2 = [1, 2, 3, 4]
y2 = lst

fig, ax = plt.subplots(2, 1)
ax[0].set_ylim(45,105)
ax[1].set_ylim(45,105)
ax[1].xaxis.set_ticks([1, 2, 3, 4])


ax[0].plot(x1, y1, color='green', linewidth = 3, marker='o', markerfacecolor='blue', markersize=8)
ax[1].plot(x2, y2, color='green', linewidth = 3, marker='o', markerfacecolor='blue', markersize=8)

ax[0].set_xlabel("Date")
ax[0].set_ylabel("Results")
ax[0].set_title('Typing Speed Averages')

ax[1].set_xlabel("Tests")
ax[1].set_ylabel("Results")
ax[1].set_title('Typing Speed Day Results')

for i,j in zip(x1,y1):
    ax[0].annotate(str(j),xy=(i,j+3))

for i,j in zip(x2,y2):
    ax[1].annotate(str(j),xy=(i,j+3))

plt.get_current_fig_manager().set_window_title('Typing Tracker')
plt.subplots_adjust(hspace = 0.8)

plt.show()
