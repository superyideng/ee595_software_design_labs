package lab10;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

class Tarjan {
    int numNodes, numEdges, numBridge = 0, cnt = 0;
    Set<Integer> nodes = new HashSet<>();
    Map<Integer, ArrayList<Integer>> undirectedGraph = new HashMap<>();
    Map<Integer, ArrayList<Integer>> directedGraph = new HashMap<>();
    Map<Integer, Integer> pre = new HashMap<>();
    Map<Integer, Integer> low = new HashMap<>();

    public void readFile(String filepath) throws IOException {
        FileInputStream fileStream = new FileInputStream(filepath);
        BufferedReader fin = new BufferedReader(new InputStreamReader(fileStream));
        numNodes = Integer.valueOf(fin.readLine());
        numEdges = Integer.valueOf(fin.readLine());
        String curLine;
        while ((curLine = fin.readLine()) != null) {
            int node1 = Integer.valueOf(curLine.trim().split(",")[0]);
            int node2 = Integer.valueOf(curLine.trim().split(",")[1]);

            // add current node to the node set
            nodes.add(node1);
            nodes.add(node2);

            // add neighbors to the adj list as the input file is undirected


            ArrayList<Integer> neighbor1 = undirectedGraph.getOrDefault(node1, new ArrayList<>());
            neighbor1.add(node2);
            undirectedGraph.put(node1, neighbor1);
            ArrayList<Integer> neighbor2 = undirectedGraph.getOrDefault(node2, new ArrayList<>());
            neighbor2.add(node1);
            undirectedGraph.put(node2, neighbor2);

            // add neighnors to the adj list as the input file is direct
            ArrayList<Integer> neighbor3 = directedGraph.getOrDefault(node1, new ArrayList<>());
            neighbor3.add(node2);
            directedGraph.put(node1, neighbor3);

        }
    }

    public int maxDegreeOfUndirected() {
        if (numNodes == 0 || numEdges == 0) {
            System.out.println("This graph has no max degree, as it has no nodes or edges.");
        }
        int maxDegree = -1;
        int maxNode = -1;
        for (int node : undirectedGraph.keySet()) {
            int curDegree = undirectedGraph.get(node).size();
            if (curDegree > maxDegree) {
                maxDegree = curDegree;
                maxNode = node;
            }
        }
        if (maxDegree > 0) {
            System.out.println("The maximum degree is " + maxDegree + " for the node number " + maxNode + ".");
        }
        return maxNode;
    }

    public void tarjan(int u, int father) {
        for (int v : nodes) {
            low.put(v, -1);
            pre.put(v, -1);
        }

        for (int v : nodes)
            if (pre.get(v) == -1)
                dfs(v, v);
    }

    private void dfs(int u, int v) {
        pre.put(v, cnt++);
        low.put(v, pre.get(v));
        for (int w : undirectedGraph.get(v)) {
            if (pre.get(w) == -1) {
                dfs(v, w);
                low.put(v, Math.min(low.get(v), low.get(w)));
                if (low.get(w).equals(pre.get(w))) {
                    if (numBridge == 0) {
                        System.out.println("This graph has bridge(s), which are shown as follows.");
                    }
                    System.out.println("--- Edge (" + v + ", " + w + ") is one bridge.");
                    numBridge++;
                }
            }

            // update low number - ignore reverse of edge leading to v
            else if (w != u)
                low.put(v, Math.min(low.get(v), low.get(w)));
        }
    }

    public List<Integer> topoSort() {
        Deque<Integer> stack = new ArrayDeque<>();
        Set<Integer> topoVis = new HashSet<>();
        for (int v : directedGraph.keySet()) {
            if (topoVis.contains(v)) {
                continue;
            }
            topoSortUtil(v, stack, topoVis);
        }
        System.out.print("One topological sort of this graph is: ");
        List<Integer> result = new ArrayList<>();
        while (!stack.isEmpty()) {
            int curr = stack.pop();
            System.out.print(curr + " -> ");
            result.add(curr);
        }
        System.out.println("end");
        return result;
    }

    private void topoSortUtil(int vertex, Deque<Integer> stack, Set<Integer> topoVis) {
        topoVis.add(vertex);
        for (int childVertex : directedGraph.getOrDefault(vertex, new ArrayList<>())) {
            if (topoVis.contains(childVertex)) {
                continue;
            }
            topoSortUtil(childVertex, stack, topoVis);
        }
        stack.offerFirst(vertex);
    }
}

public class lab10_part2 {
    public static void main(String[] args) throws IOException{
        for (int _n = 0; _n < 20; _n++) {
            System.out.println("For Graph" + _n + ":");
            TreeChecker tc = new TreeChecker();
            tc.readFile("graph" + _n + ".txt");
            boolean isTree = tc.treeChecker();

            Tarjan tarj = new Tarjan();
            tarj.readFile("graph" + _n + ".txt");
            tarj.maxDegreeOfUndirected();
            tarj.tarjan(0, -1);
            if (tarj.numBridge == 0) {
                System.out.println("This graph has no bridge.");
            }
            if (isTree) {
                tarj.topoSort();
            }
            System.out.println();
        }
    }
}
