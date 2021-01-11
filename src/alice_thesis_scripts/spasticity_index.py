from extract_sto import *
import numpy as np
import matplotlib.pyplot as plt


def all_cycles_spasticity_index(sto_file, side, plot=True):
    """
    Computes spasticity index as the ratio of SOL activation peak over SOL stretch velocity peak during swing phase
    for all gait cycles and average, plots SOL activation and stretch velocity during gait cycle
    INPUTS: - sto_file: path to sto file of interest
            - side: 'r' or 'l' for right or left variables
            - plot: plot if True
   OUTPUTS: - spasticity_ind: spasticity index
    """

    var_names, var_tab = extract_sto(sto_file)
    lstance_starts, lstance_ends, rstance_starts, rstance_ends = stance_phase_indexes(var_names, var_tab)

    if side == 'l':
        stance_starts = lstance_starts
        stance_ends = lstance_ends
    else:
        stance_starts = rstance_starts
        stance_ends = rstance_ends

    sol_acti_index = np.where(var_names == 'soleus_'+side+'.activation')[0][0]
    sol_stretchv_index = np.where(var_names == 'soleus_'+side+'.mtu_velocity')[0][0]
    time = var_tab[:, 0]
    sol_acti = var_tab[:, sol_acti_index]
    sol_stretchv = var_tab[:, sol_stretchv_index]

    if plot:
        fig, ax = plt.subplots()
        if stance_starts[0] < stance_ends[0]:
            ax.axvspan(0, time[stance_starts[0]], alpha=0.5, color='bisque', label=side+'swing')
            for t in range(len(stance_starts) - 1):
                ax.axvspan(time[stance_ends[t]], time[stance_starts[t + 1]], alpha=0.5, color='bisque')
        else:
            for t in range(len(stance_starts)-1):
                ax.axvspan(time[stance_ends[t]], time[stance_starts[t]], alpha=0.5, color='bisque')
            t = len(stance_starts) - 1
            ax.axvspan(time[stance_ends[t]], time[stance_starts[t]], alpha=0.5, color='bisque', label=side+'swing')
        ax.plot(time, sol_acti, 'brown', label=side+'SOL activation')
        ax.plot(time, sol_stretchv, 'b', label=side+'SOL stretch velocity')
        ax.legend(loc='upper right')
        ax.set_xlabel('gait cycle [s]')
        ax.set_title(side+'SOL activation and stretch velocity during gait')
        plt.show()

        plt.figure()
        plt.plot(sol_stretchv, sol_acti, 'b', label=side+'stance')
        if stance_starts[0] < stance_ends[0]:
            plt.plot(sol_stretchv[0:stance_starts[0]], sol_acti[0:stance_starts[0]], 'brown', label='Lswing')
            for t in range(len(stance_starts) - 1):
                plt.plot(sol_stretchv[stance_ends[t]:stance_starts[t + 1]],
                         sol_acti[stance_ends[t]:stance_starts[t + 1]], 'brown')
        else:
            for t in range(len(stance_starts) - 1):
                plt.plot(sol_stretchv[stance_ends[t]:stance_starts[t]],
                         sol_acti[stance_ends[t]:stance_starts[t]], 'brown')
            t = len(stance_starts) - 1
            plt.plot(sol_stretchv[lstance_ends[t]:lstance_starts[t]],
                     sol_acti[lstance_ends[t]:lstance_starts[t]], 'brown', label=side+'swing')
        plt.legend()
        plt.xlabel(side+'SOL stretch velocity')
        plt.ylabel(side+'SOL activation')
        plt.title('')
        plt.show()

    # spasticity index computation
    if stance_starts[0] < stance_ends[0]:
        spasticity_indexes = np.zeros(len(stance_starts)-1)
        for t in range(len(stance_starts)-1):
            swing_sol_acti = sol_acti[stance_ends[t]:stance_starts[t + 1]]
            swing_sol_stretchv = sol_stretchv[stance_ends[t]:stance_starts[t+1]]
            spasticity_indexes[t] = max(swing_sol_acti) / max(swing_sol_stretchv)
    else:
        spasticity_indexes = np.zeros(len(stance_starts))
        for t in range(len(stance_starts)):
            swing_sol_acti = sol_acti[stance_ends[t]:stance_starts[t]]
            swing_sol_stretchv = sol_stretchv[stance_ends[t]:stance_starts[t]]
            spasticity_indexes[t] = max(swing_sol_acti) / max(swing_sol_stretchv)

    spasticity_ind = np.mean(spasticity_indexes)

    return spasticity_ind


def mean_cycle_spasticity_index(sto_file, side, plot=True):
    """
    Computes spasticity index as the ratio of SOL activation peak over SOL stretch velocity peak during swing phase
    for averaged gait cycle, plots SOL activation and stretch velocity during gait cycle
    INPUTS: - sto_file: path to sto file of interest
            - side: 'r' or 'l' for right or left variables
            - plot=True: plot if True
    OUTPUTS: - spasticity_ind: spasticity index
    """

    var_names, var_tab = extract_sto(sto_file)

    time = var_tab[:, 0]
    av_stance_sol_acti, av_swing_sol_acti, av_gait_cycle, av_stance_end = mean_gait_phases(var_names, var_tab,
                                                                                           'soleus_'+side+'.activation',
                                                                                           side)
    av_stance_sol_stretchv, av_swing_sol_stretchv, av_gait_cycle, av_stance_end = mean_gait_phases(var_names, var_tab,
                                                                                                   'soleus_'+side+
                                                                                                       '.mtu_velocity',
                                                                                                       side)
    if plot:
        if side == 'r':
            side_name = 'Right'
        elif side == 'l':
            side_name = 'Left'
        mean_sol_acti = np.concatenate((av_stance_sol_acti, av_swing_sol_acti, av_stance_sol_acti))
        mean_sol_stretchv = np.concatenate((av_stance_sol_stretchv, av_swing_sol_stretchv,
                                            av_stance_sol_stretchv))
        fig, ax = plt.subplots()
        ax.plot(time[:av_gait_cycle+av_stance_end]*100/time[av_gait_cycle], mean_sol_acti, 'brown',
                label=side_name+' SOL activation')
        ax.plot(time[:av_gait_cycle+av_stance_end]*100/time[av_gait_cycle], mean_sol_stretchv, 'b',
                label=side_name+' SOL stretch velocity')
        ax.axvspan(time[av_stance_end]*100/time[av_gait_cycle], time[av_gait_cycle]*100/time[av_gait_cycle], alpha=0.5,
                   color='bisque', label=side_name+' swing')
        ax.legend(loc=3)
        ax.set_xlabel('Gait cycle (%)')
        ax.set_ylabel('SOL activation () \n/ Stretch velocity (m/s)')
        ax.set_title(side_name+' SOL activation and stretch velocity during gait')
        plt.show()

    spasticity_ind = np.max(av_swing_sol_acti)/np.max(av_swing_sol_stretchv)

    return spasticity_ind
