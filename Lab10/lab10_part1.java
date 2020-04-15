package lab10;
import edu.princeton.cs.algs4.MSD;

import javax.print.attribute.IntegerSyntax;
import java.io.*;
import java.util.*;

class TreeChecker {
    int numNodes, numEdges;
    Set<Integer> nodes = new HashSet<>();
    Map<Integer, ArrayList<Integer>> undirectedGraph = new HashMap<>();
    Map<Integer, ArrayList<Integer>> directedGraph = new HashMap<>();
    Set<Integer> visited = new HashSet<>();

    TreeChecker (){
        visited = new HashSet<>();
    }

    public void readFile(String filepath) throws IOException{
        FileInputStream fileStream = new FileInputStream(filepath);
        BufferedReader fin = new BufferedReader(new InputStreamReader(fileStream));
        numNodes = Integer.valueOf(fin.readLine());
        numEdges = Integer.valueOf(fin.readLine());
        String curLine;
        while ((curLine = fin.readLine()) != null && curLine.length() != 0) {
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

    public boolean treeChecker() {
        if (numNodes == 0 || numEdges == 0) {
            System.out.println("This graph is not a tree, as it has no nodes or edges inside.");
            return false;
        }
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

    private boolean helper(int curr, int parent, ArrayList<Integer> path) {
        if (visited.contains(curr)) {
            System.out.print("This graph is not a tree. A loop in this graph is: ");
            int iStart = 0;
            while (iStart < path.size()) {
                if (path.get(iStart) == curr) break;
                iStart++;
            }
            for (int _k = iStart; _k < path.size(); _k++) {
                System.out.print(path.get(_k) + " ");
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
}

class GraphGenerator {
    int fileNo = 0;

    void generate() throws IOException {
        String curGraphName = "graph" + fileNo + ".txt";
        BufferedWriter out = new BufferedWriter(new FileWriter(curGraphName));

        if (fileNo == 0) { // generate graph with 0 edge and 0 node
            out.write("0\n");
            out.write("0\n");
        } else if (fileNo == 1) { // generate fully connected graph with more than 4 nodes
            int numNodes = 4 + (int)(Math.random() * 7);
            int numEdges = numNodes * (numNodes - 1) / 2;
            out.write(numNodes + "\n");
            out.write(numEdges + "\n");
            for (int i = 0; i < numNodes; i++) {
                for (int j = i + 1; j < numNodes; j++) {
                    out.write(i + "," + j + "\n");
                }
            }
        } else if (fileNo == 2) { // generate graph with at least 5 nodes, and exactly 2 edges
            int numNodes = 5 + (int)(Math.random() * 6);
            out.write(numNodes + "\n");
            out.write("2\n");
            Set<String> edges = new HashSet<>();
            while (edges.size() < 2) {
                int node1 = (int)(Math.random() * (numNodes));
                int node2 = node1 + (int)(Math.random() * (numNodes - node1));
                String curEdge = node1 + "," + node2;
                if (node1 != node2) {
                    edges.add(curEdge);
                }
            }
            for (String cur : edges) {
                out.write(cur + "\n");
            }
        } else {
            int numNodes = (int)(Math.random() * 11);
            int numEdges = (int)(Math.random() * (numNodes * (numNodes - 1) / 3));
            out.write(numNodes + "\n");
            out.write(numEdges + "\n");
            Set<String> edges = new HashSet<>();
            while (edges.size() < numEdges) {
                int node1 = (int)(Math.random() * (numNodes));
                int node2 = node1 + (int)(Math.random() * (numNodes - node1));
                String curEdge= "" + node1 + "," + node2;
                if (node1 != node2 && !edges.contains(curEdge)) {
                    edges.add(curEdge);
                }
            }
            for (String cur : edges) {
                out.write(cur + "\n");
            }
        }
        out.close();
        System.out.println("Graph No." + fileNo + " has generated sucessfully!");
        fileNo++;
    }
}

public class lab10_part1 {
    public static void main(String[] args) throws IOException{
        GraphGenerator gg = new GraphGenerator();
        for (int _n = 0; _n < 20; _n++) {
            gg.generate();
            TreeChecker tc = new TreeChecker();
            tc.readFile("graph" + _n + ".txt");
            tc.treeChecker();
        }
    }
}
