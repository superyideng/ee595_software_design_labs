import java.io.*;
import java.util.*;

public class Main {
    private static int numNodes, numEdges, numBridge = 0, cnt = 0;
    private static HashSet<Integer> nodes = new HashSet<>();
    private static HashMap<Integer, ArrayList<Integer>> undirectedGraph = new HashMap<>();
    private static HashMap<Integer, ArrayList<Integer>> directedGraph = new HashMap<>();
    private static HashSet<Integer> visited = new HashSet<>();
    private static HashMap<Integer, Integer> pre = new HashMap<>();
    private static HashMap<Integer, Integer> low = new HashMap<>();

    private static void readFile(String filepath) throws IOException{
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

    private static boolean treeChecker() {
        int curr = nodes.iterator().next();
        if (!helper(curr, -1, new ArrayList<>())) {
            return false;
        }
        if (visited.size() != numNodes) {
            System.out.println("This graph is not a tree, as it is not connected.");
            return false;
        }

        System.out.println("This graph is a tree, it is connected and has no loop inside.");
        return true;
    }

    private static boolean helper(int curr, int parent, ArrayList<Integer> path) {
        if (visited.contains(curr)) {
            System.out.print("This graph is not a tree. A loop in this graph is: ");
            for (int node : path) {
                System.out.print(node + " ");
            }
            System.out.println(curr);
            return false;
        }

        visited.add(curr);

        for (int i : undirectedGraph.get(curr)) {
            path.add(curr);
            if (i != parent && !helper(i, curr, path)) {
                return false;
            }
            path.remove(path.size() - 1);

        }

        return true;
    }

    private static int maxDegreeOfUndirected() {
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

    private static void tarjan(int u, int father) {
        for (int v : nodes) {
            low.put(v, -1);
            pre.put(v, -1);
        }

        for (int v : nodes)
            if (pre.get(v) == -1)
                dfs(v, v);
    }

    private static void dfs(int u, int v) {
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
                    StdOut.println("--- Edge (" + v + ", " + w + ") is one bridge.");
                    numBridge++;
                }
            }

            // update low number - ignore reverse of edge leading to v
            else if (w != u)
                low.put(v, Math.min(low.get(v), low.get(w)));
        }
    }

    private static List<Integer> topoSort() {
        Deque<Integer> stack = new ArrayDeque<>();
        Set<Integer> topoVis = new HashSet<>();
        for (int v : directedGraph.keySet()) {
            if (topoVis.contains(v)) {
                continue;
            }
            topoSortUtil(v, stack, topoVis);
        }
        System.out.print("One topological sort of the graph is: ");
        List<Integer> result = new ArrayList<>();
        while (!stack.isEmpty()) {
            int curr = stack.pop();
            System.out.print(curr + " -> ");
            result.add(curr);
        }
        System.out.println("end");
        return result;
    }

    private static void topoSortUtil(int vertex, Deque<Integer> stack, Set<Integer> topoVis) {
        topoVis.add(vertex);
        for (int childVertex : directedGraph.getOrDefault(vertex, new ArrayList<>())) {
            if (topoVis.contains(childVertex)) {
                continue;
            }
            topoSortUtil(childVertex, stack, topoVis);
        }
        stack.offerFirst(vertex);
    }

//    private static void maxClique() {
//
//    }


    public static void main(String[] args) throws IOException{
        String path = "input_p1.txt";
        readFile(path);
        boolean isTree = treeChecker();
        maxDegreeOfUndirected();
        tarjan(nodes.iterator().next(), -1);
        if (numBridge == 0) {
            System.out.println("This graph has no bridges.");
        }
        if (isTree) {
            topoSort();
        }
    }
}
