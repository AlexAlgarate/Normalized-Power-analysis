import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('pareja.csv')
df.drop(['headwind', 'slope', 'temp', 'lrbalance',
         'hhb', 'thb', 'o2hb', 'lte', 'rte', 'smo2',
         'rps', 'lon', 'hr', 'lat', 'interval',
         'lps', 'nm'], axis=1, inplace=True)


'''print(df.describe()) #Basic descriptive statistics'''

# Step 1: Take the moving 30s avg POWER data (or 25s avg.)
# Step 2: Raise each value to the 4th power
# Step 3: Find the average of the values from the preivous step
# Step 4: Take the  4th root of the mean value in the previous step.
'''print()
df['M30'] = df['watts'].rolling(window=30).mean() #Step 1
df['M30_cuarta'] = df['M30']**4 #Step 2
df['NPower'] = (df['M30_cuarta'].mean())**(1/4) #Step 3 & 4'''

df['NPower'] = np.sqrt(np.sqrt(np.mean(df['watts'].rolling(window=25).mean()**4)))
df['w_MA30'] = df['watts'].rolling(window=25).mean()  # Step 1
df['w_avg30_4power'] = df['w_MA30']**4
df.drop(df.index[0:30], inplace=True)
df['w_avg30_4power_avg'] = df['w_avg30_4power'].rolling(window=30).mean()
df.drop(df.index[0:30], inplace=True)
df['4root'] = df['w_avg30_4power_avg']**(0.25)
pot_normalizada = df['4root'].mean()

'''def cycling_norm_power(Power): #Función para la NP

    WindowSize = 30; # second rolling average

    NumberSeries = pd.Series(Power)
    NumberSeries = NumberSeries.dropna()
    Windows      = NumberSeries.rolling(WindowSize)
    Power_30s    = Windows.mean().dropna()

    PowerAvg     = round(Power_30s.mean(),0)

    NP = round((((Power_30s**4).mean())**0.25),0)
    return(NP,PowerAvg)'''

print()
print(f"La potencia normalizada fue de {pot_normalizada:.2f} W")
print()
print(df.head(50))

npw = np.sqrt(np.sqrt(np.mean(df['watts'].rolling(25).mean()**4)))
print(f"La potencia normalizada del Triatlon de Pareja fue de {npw:.2f} W")
print()

# Graph results
'''
df['watts'].plot(figsize=(10,6), linewidth=0.65, color='r')
df['watts'].rolling(window=25).mean().plot()
plt.show()
'''

fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

ax1.plot(df['watts'], lw=0.55, c='r',
         alpha=0.3, label='W_1sec')  # Line of 1s watts
'''ax1.plot(df['NPower'], lw=1.5, c='indigo',
         label='W_NP') #Line of Normalized POwer
ax1.plot(df['w_MA30'], lw=0.75, c='blue',
         alpha=0.5, label='W_30sec') #Line of Moving Average 30s'''
ax1.plot(df['4root'], lw=2, c='indigo',
         label='NP_30sMA')  # Line of the 4th root = NP (Step4)

ax2.plot(df['alt'], lw=0.75, c='green', label='Altitude')  # Altitude
# Fill the area below the curve altitude
plt.fill_between(df['secs'], df['alt'],
                 720, facecolor='g', alpha=0.05)

# Keep lines and labels from AX1 and AX2
lines, labels = [(a + b) for a, b in zip(ax1.get_legend_handles_labels(),
                                         ax2.get_legend_handles_labels())]
ax1.legend(lines, labels,
           loc='upper right')  # Print them together inside the plot.

ax1.set_xlabel('Seconds')
ax1.set_ylabel('Power (w)')
ax2.set_ylabel('Altitude (m)')
ax1.set_title("Bike course analysis from Pareja Triathlon")

plt.show()


# Power zones
# z1 Active recovery --> Less than 55%
# z2 Endurance --> 69-83%	56-75% ;; more than 3h
# z3 Tempo / Sweetspot --> 84-94%	76-90% ;; 20 mins to 1 hour
# z4 Threshold --> 95-105%	91-105% ;; 10 to 30 mins
# z5 VO2 max --> More than 106%	106-120% ;; 3 to 8 mins
# z6 Anaerobic capacity --> n/a	More than 121% ;; 30 seconds to 3 mins
# z7 neuromuscular --> More than 151%  ;; 10  to 30 second sprints
cp = 313  # Critical Power
# Crear 7 columnas, NAN donde no se cumpla la condición de potencia ??

df['watts'].plot(kind='hist', color='r', alpha=0.40, label="Watts Freq.")
plt.xlabel('Seconds')
plt.ylabel('Power(w)')
plt.title('Power distribution Pareja Triatlon')
plt.legend(loc=7)  # Location: Center right
plt.show()

'''df1 = df['watts']
ax3 = df1.plot.hist(figsize=(10, 6), bins=7,
                    color='blue', alpha=0.45, label='Power Zones')
plt.title("Power Zones Pareja's Triathlon")
plt.xlabel('Power(w)')
plt.show()'''
