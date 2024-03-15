#作用力为F，ER网络，20次
#学习热力图1-1
#F
import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np

def simulate_SIR_on_ER(N, p, beta, F, a4):
    # 初始化ER网络
    G = nx.erdos_renyi_graph(N, p)

    # 随机选择一个初始感染者
    I0 = 20
    
    # 初始化SIR状态
    I = set(random.sample(G.nodes(), I0))
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

def plot_heatmap(N, p, a4, num_simulations=20):
    beta_values = np.linspace(0, 1, 101)  # beta 取值范围为 0-1，共 101 个点
    F_values = np.linspace(0, 1, 101)  # F 取值范围为 0-1，共 101 个点
    z_values = np.zeros((101, 101))  # 初始化感染率矩阵

    for i, F in enumerate(F_values):
        for j, beta in enumerate(beta_values):
            total_infectious_ratio = 0
            for k in range(num_simulations):
                infectious_ratio = simulate_SIR_on_ER(N, p, beta,1-F, a4)
                total_infectious_ratio += infectious_ratio
            z_values[i, j] = total_infectious_ratio / num_simulations
            
            
    np.savetxt('N2000_1.txt', z_values)
    
    # 绘制热力图
    plt.imshow(z_values,cmap='YlGnBu_r', extent=[0, 1, 0, 1], aspect='auto')
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=18) # 可以使用具体的数值来替换'large'
    plt.xlabel(r'$\alpha_{1}$',fontsize=22)
    plt.ylabel('F',fontsize=22)
    plt.xticks(fontproperties = 'Times New Roman', size = 22)
    plt.yticks(fontproperties = 'Times New Roman', size = 22)
    plot_y()
    plt.show()

def average_degree():
    G = nx.erdos_renyi_graph(2000, 0.003)
    average_degree = sum(dict(G.degree()).values()) / len(G)
    return average_degree
    print("Average degree:", average_degree)
    
def plot_y():
    x=np.linspace(0, 1, 101)    
    y=1/(average_degree()*x)
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.plot(x,y,"--",linewidth=2,color="White")



# 主函数
def main():
    N = 2000
    p = 0.003
    a4 = 1
    num_simulations = 20
    plot_heatmap(N, p, a4, num_simulations)

if __name__ == '__main__':
    main()