# SimpleTSP
Simple modified traveling salesman solution.

## Modified TSP
In this problem we want a minimum path length through any N points, not a cycle throw certain points.

## Bounded Search
We begin with a greedy solution starting with each point, and pick the smallest. This is our upperbound. We will stop searching if the solution would not be better than this.

Then, we simply depth first search through all the points. Early stopping and updating the upper bound when we find a better path.

### Improvements
Given that this style of solution is still only suitable for relatively small sets of points. It is likely worthwhile to keep track of a lower bound path length for remaining points while we search. This way we could stop our searching much earlier on low performing paths. This tracking could be as simple as keeping a nearest neighbor for each point or more complex to keep track of the shortest edge to an unexplored neighbor.
