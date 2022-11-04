### The Ripple-Spreading Algorithm for Co-Evolutionary Path Optimization

##### Reference: HU X B,ZHANG M K,ZHANG Q,et al.Co-evolutionary path optimization by ripple-spreading algorithm[J].Transportation Research:Part B,2017,106:411-432.

The k shortest paths problem aims to find the shortest path between two nodes in a dynamic network. 

| Variables     | Meaning                                                      |
| ------------- | ------------------------------------------------------------ |
| network       | Dictionary, {node 1: {node 2: [weight 1, weight 2, ...], ...}, ...} |
| s_network     | The network described by a crisp weight on which we conduct the ripple relay race |
| source        | The source node                                              |
| destination   | The destination node                                         |
| k             | The *k* shortest paths                                       |
| orad          | The radius of the obstacle                                   |
| ospeed        | The moving speed of the obstacle                             |
| nn            | The number of nodes                                          |
| neighbor      | Dictionary, {node1: [the neighbor nodes of node1], ...}      |
| v             | The ripple-spreading speed (i.e., the minimum length of arcs) |
| t             | The simulated time index                                     |
| nr            | The number of ripples - 1                                    |
| epicenter_set | List, the epicenter node of the i-th ripple is epicenter_set[i] |
| path_set      | List, the path of the i-th ripple from the source node to node i is path_set[i] |
| radius_set    | List, the radius of the i-th ripple is radius_set[i]         |
| state_set     | List, state_set[i] = 1, 2, or 3 means the ripple i is waiting, active, or dead |
| objective_set | List, the objective value of the traveling path of the i-th ripple is objective_set[i] |
| omega         | Dictionary, omega[n] contains all ripples generated at node n |

#### Example

![CEPO](C:\Users\dell\Desktop\研究生\个人算法主页\The ripple-spreading algorithm for the co-evolutionary path optimization\CEPO.gif)

The obstacle moves from the lower right corner to the upper right corner with radius = orad and speed = ospeed. The shortest path length is 164.56956372198448.

```python
if __name__ == '__main__':
    network, x, y = init_network()  # the grid network has 100 nodes
    s = 0  # lower left corner
    d = 99  # upper right corner
    orad = 15  # obstacle radius
    ospeed = 6  # obstacle speed
    print(main(network, s, d, x, y, orad, ospeed))
```

##### Output:

```python
{
    'shortest path': [0, 10, 11, 12, 22, 32, 42, 43, 54, 64, 65, 75, 86, 87, 88, 98, 99], 
    'length': 164.56956372198448
}
```

