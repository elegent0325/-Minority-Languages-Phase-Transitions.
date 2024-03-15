#阈值图，在ER网络上，N=2000,20/2000=1%，度为6
#正确的图，论文中的实例1；F=0.4,0.6,1
import networkx as nx
import random
import matplotlib.pyplot as plt

beta_values = []
infectious_ratios = []


def simulate_SIR_on_ER(N, p, beta, F, a4):
    # 初始化ER网络
    G = nx.erdos_renyi_graph(N, p)

    # 随机选择一个初始感染者
    I0=20
    
    # 初始化SIR状态
    I = set(random.sample(G.nodes(),I0))
    S = set(G.nodes()) - I
    R = set()

    while len(I) > 0:
        # 传播过程
        new_infected = set()
        for infected_node in I:
            neighbors = set(G.neighbors(infected_node))
            susceptible_neighbors = neighbors.intersection(S)
            for neighbor in susceptible_neighbors:
                if random.random() < beta*F:
                    new_infected.add(neighbor)
            if random.random() < a4:
                R.add(infected_node)
            else:
                new_infected.add(infected_node)
        I = new_infected
        S = S - I

    # 计算传染率
    infectious_ratio = len(R) / N

    return infectious_ratio

def plot_beta_vs_I(N, p, F, a4, num_simulations=20, beta_step=0.01, marker='o',markerfacecolor='none', linestyle=''):
    beta_values = []
    infectious_ratios = []
    beta = 0
    while beta < 1:
        beta += beta_step
        beta_values.append(beta)
        total_infectious_ratio = 0
        for i in range(num_simulations):
            infectious_ratio = simulate_SIR_on_ER(N, p, beta, F, a4)
            total_infectious_ratio += infectious_ratio
        infectious_ratio = total_infectious_ratio / num_simulations
        infectious_ratios.append(infectious_ratio)
        
    plt.plot(beta_values, infectious_ratios, marker=marker, linestyle="-",label=f'{"Positive" if F==0.4 else "Negative" if F==0.6 else "No"} interaction')


# 主函数


def main():
    N = 2000
    p = 0.003
    a4 = 1
    num_simulations = 20
    beta_step = 0.01
    F_list = [0.4, 0.6, 1.0]
    #labels={0.4: 'positive interaction"', 0.6: 'negative interaction', 1.0: 'no interaction'}
    markers = {0.4: 'o', 0.6: 's', 1.0: 'v'}
    #linestyles = {0.4: '--', 0.6: '--',1.0: '--'}
    plt.figure(figsize=(6, 6))

    for i, F in enumerate(F_list):
        marker = markers[F]
        #linestyle = linestyles[F]
        plot_beta_vs_I(N, p, F, a4, num_simulations, beta_step, marker=marker, linestyle=" ")
    
    plt.xlabel(r"$\alpha_{1}$",fontsize=26)
    plt.ylabel('z',fontsize=26)
    plt.xticks(fontproperties = 'Times New Roman', size = 26)
    plt.yticks(fontproperties = 'Times New Roman', size = 26)
    plt.legend(fontsize=12)
    plt.xlim(0,0.6)
    plt.ylim(0,1)
    plt.show()

if __name__ == '__main__':
    main()