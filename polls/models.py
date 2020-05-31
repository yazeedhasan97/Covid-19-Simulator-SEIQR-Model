import os, datetime
from scipy import integrate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns


# from django.db import models
# from matplotlib.animation import FuncAnimation
# import matplotlib.animation as animation



matplotlib.rc('figure', figsize=(12, 8))
sns.set()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Inputs:
    def __init__(self):
        pass


class OutputForm:
    def __init__(
            self, sick_undiagnosed,
            sick_all_time,
            sick_diagnosed,
            recovered_diagnosed,
            recovered_never_diagnosed,
            deceased):
        self.sick_undiagnosed = sick_undiagnosed
        self.sick_all_time = sick_all_time
        self.sick_diagnosed = sick_diagnosed
        self.recovered_diagnosed = recovered_diagnosed
        self.recovered_never_diagnosed = recovered_never_diagnosed
        self.deceased = deceased


class CalculationModel:
    def __init__(self, inputs):
        self.inputs = inputs
        self.graph_data = np.array([])
        self.time = []
        self.final_death_number = 0
        initials = [self.inputs.susceptible, self.inputs.quarantine, self.inputs.exposed, self.inputs.infected,
                    self.inputs.recovered]
        time_line = (0, self.inputs.tf)
        others = integrate.solve_ivp(self.SEIQR, time_line, initials)

        # rng = pd.date_range('2020-01-1', '2020-12-31', freq='D')
        time = others['t']
        susceptible = others['y'][0]
        exposed = others['y'][1]
        quarantine = others['y'][3]
        infected = others['y'][2]
        recovered = others['y'][4]

        df = pd.DataFrame({
            # 'Date': rng,
            'Time': time,
            'Susceptible': susceptible,
            'Exposed': exposed,
            'Infected': infected,
            'Quarantine': quarantine,
            'Recovered': recovered
        })

        # path = BASE_DIR + f'/static/files/DataCase_{datetime.datetime.now():%Y%m%d%H%M}.csv'
        # df.to_csv(path, index=False)

        self.plot_outputs(others['t'], others['y'])

    def SEIQR(self, t, x):
        return np.array(
            [self.inputs.b - self.inputs.beta * x[0] * x[2] + self.inputs.zeta * x[4] - self.inputs.d * x[0],
             self.inputs.beta * x[0] * x[2] - (self.inputs.gamma + self.inputs.xi) * x[1] - self.inputs.d * x[1],
             self.inputs.gamma * x[1] - (self.inputs.epsilon + self.inputs.delta) * x[2] - (self.inputs.mu + self.inputs.d) * x[2],
             self.inputs.delta * x[2] - self.inputs.theta * x[3] - (self.inputs.mu + self.inputs.d) * x[3],
             self.inputs.epsilon * x[2] + self.inputs.theta * x[3] + self.inputs.xi * x[1] - self.inputs.zeta * x[4] - self.inputs.d * x[4]])



    def plot_outputs(self, time, y_outputs):
        death = (y_outputs[2].astype('int') + y_outputs[3].astype('int')) * self.inputs.mu

        total_number_of_patients = np.ones(len(time)) * self.inputs.hospital_number * self.inputs.nurse_ber_hospital * self.inputs.max_nurse_handel
        total_number_of_beds = np.ones(len(time)) * self.inputs.hospital_number * self.inputs.beds_ber_hospital

        fig = plt.figure()
        for i in range(5):
            plt.plot(time, y_outputs[i])
        plt.plot(time, death)
        plt.plot(time, total_number_of_beds - y_outputs[3])
        plt.plot(time, total_number_of_patients - y_outputs[2])

        lg = ['Susceptible', 'Exposed', 'Infected', 'Quarantine', 'Recovered', 'Death',
              'Total Number Of Available Beds', 'Total Number Of Patients to handle']  #
        plt.xlabel('Time Unit')
        plt.ylabel('Number Of People')
        step = self.inputs.tf // 10
        plt.xticks(ticks=[i for i in range(1, self.inputs.tf + step, step)],
                   labels=[f'D{i}' for i in range(1, self.inputs.tf + step, step)], rotation=45, fontsize=10)
        plt.legend(lg)

        plt.savefig(BASE_DIR + '\static\my_app\sss.png')



