package lab10;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

class MaxClique {

    int MAX = 20, numNodes, numEdges;

    // Stores the vertices
    int[] store = new int[MAX];

    // Graph
    int[][] graph = new int[MAX][MAX];

    // Degree of the vertices
    int[] degree = new int[MAX];

    int numNodeInClique;

    int[] nodeInClique;

    public void readFile(String filepath) throws IOException {
        FileInputStream fileStream = new FileInputStream(filepath);
        BufferedReader fin = new BufferedReader(new InputStreamReader(fileStream));
        numNodes = Integer.valueOf(fin.readLine());
        numEdges = Integer.valueOf(fin.readLine());
        String curLine;
        while ((curLine = fin.readLine()) != null && curLine.length() != 0) {
            int node1 = Integer.valueOf(curLine.trim().split(",")[0]);
            int node2 = Integer.valueOf(curLine.trim().split(",")[1]);

            graph[node1][node2] = 1;
            graph[node2][node1] = 1;
            degree[node1]++;
            degree[node2]++;
        }
    }

    // check if the given set of vertices in the store array is a clique or not
    private boolean isClique(int b) {
        // Run a loop for all set of edges
        for (int i = 1; i < b; i++) {
            for (int j = i + 1; j < b; j++)

                // If any edge is missing
                if (graph[store[i]][store[j]] == 0)
                    return false;
        }
        return true;
    }

    // find all the sizes of maximal cliques
    public int maxCliques(int i, int l) {
        // Maximal clique size
        int maxNumNode = 0;

        // Check if any vertices from  i+1 can be inserted
        for (int j = i + 1; j <= numNodes; j++) {
            // Add the vertex to store
            store[l] = j;

            // If the graph is not a clique of size k then it cannot be a clique by adding another edge
            if (isClique(l + 1)) {
                // Update max
                if (l > numNodeInClique) {
                    numNodeInClique = l;
                    nodeInClique = store.clone();
//                    for (int n : nodeInClique) {
//                        System.out.print(n);
//                    }
//                    System.out.println();
                }
                maxNumNode = Math.max(maxNumNode, l);

                // Check if another edge can be added
                maxNumNode = Math.max(maxNumNode, maxCliques(j, l + 1));
            }
        }
        return maxNumNode;
    }
}

public class lab10_part3 {
    // Driver code
    public static void main(String[] args) throws IOException {
        for (int _n = 0; _n < 20; _n++) {
            System.out.println("For Graph" + _n + ":");
            MaxClique mc = new MaxClique();
            mc.readFile("graph" + _n + ".txt");
            mc.maxCliques(-1, 1);
            System.out.print("The max clique has " + mc.numNodeInClique + " node(s) in it: ");
            for (int i = 1; i < mc.numNodeInClique + 1; i++) {
                System.out.print(mc.nodeInClique[i] + " ");
            }
            System.out.println();
        }
    }
}