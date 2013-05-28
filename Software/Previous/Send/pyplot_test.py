import matplotlib.pyplot as plt
plt.ion()
plt.figure(1)                # the first figure
plt.subplot(211)             # the first subplot in the first figure
plt.plot([1,2,3])
plt.subplot(212)             # the second subplot in the first figure
plt.plot([4,5,6])

plt.figure(2)                # a second figure
plt.plot([4,5,6])            # creates a subplot(111) by default

raw_input("Continue...")

plt.figure(1)                # figure 1 current; subplot(212) still current
plt.subplot(211)             # make subplot(211) in figure1 current
plt.title('Easy as 1,2,3')   # subplot 211 title

raw_input("Press enter when done...")

