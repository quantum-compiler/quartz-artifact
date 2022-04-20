import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import ast


n_min = 2
n_max = 7
d = []
for n in range(n_min, n_max + 1):
    with open(f'Nam_{n}_3_iterations.log', 'r') as f:
        data = f.read()
        d.append(ast.literal_eval(data))


plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

original_val = [900, 58, 114, 170, 450, 170, 420, 225, 347, 495, 669, 883, 1095, 1347, 63, 119, 278, 521, 443, 884, 200, 45, 75, 105, 255, 150]

# geomean_reduction = []
# for i in range(num_timestamps):
#     geomean = 1
#     for circuit_name, _ in d[0].items():
#         maxval = 0
#         for q in range(len(d)):
#             maxval = max(maxval, d[q][circuit_name][i])
#         geomean *= 1 - maxval
#     geomean = 1 - geomean ** (1 / 26)
#     geomean_reduction.append(geomean)

labels = [
'n=2',
'n=3',
'n=4',
'n=5',
'n=6',
'n=7',
'best',
]

cnt = 0
for circuit_name, _ in d[0].items():
    plt.cla()
    plt.figure(constrained_layout=True)
    plt.xlabel('Search Iterations for q=3', fontsize=12, fontweight='bold')
    plt.xticks(fontsize=12)
    plt.ylabel('Gate Count Reduction', fontsize=12, fontweight='bold')
    plt.gca().set_xscale('log')
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=1))
    plt.yticks(fontsize=12)
    for q in range(len(d)):
        reduction = d[q][circuit_name]
        plt.plot(range(len(reduction)), reduction, ['x-', '+-', '.--', 's-', '*-', 'o-'][q], markersize=7, label=labels[q],
                 markevery=[0.4, 0.38, 0.32, 0.35, 0.33, 0.45][q])
    fig = plt.gcf()
    plt.legend(fontsize=12, ncol=2)
    fig.set_size_inches(5.2, 3.6)
    fig.savefig(f'iteration_plot_{circuit_name}.pdf', dpi=800)
    circuit_name_escaped = circuit_name.replace('_', '\_').replace('^', '\^{}')
    print(f'''
\\begin{{figure}}
\\centering
\\includegraphics[width=\evalfigfrac\linewidth]{{figures/appendix/iteration_plot_{circuit_name}.pdf}}
\\caption{{\\texttt{{{circuit_name_escaped}}} ({original_val[cnt]} gates).}}
\\label{{fig:time:{circuit_name}}}
\\end{{figure}}
''')
    cnt += 1
    plt.close()
