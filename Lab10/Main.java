import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

public class Main {
    private static int numNodes;
    private static int numEdges;
    private static HashMap<Integer, ArrayList<Integer>> map = new HashMap<>();
    private static HashSet<Integer> visited = new HashSet<>();

    public static void readFile(String filepath) throws IOException{
        FileInputStream fileStream = new FileInputStream(filepath);
        BufferedReader fin = new BufferedReader(new InputStreamReader(fileStream));
        numNodes = Integer.valueOf(fin.readLine());
        numEdges = Integer.valueOf(fin.readLine());
        System.out.println(numEdges);
        String curLine;
        while ((curLine = fin.readLine()) != null) {
            int node1 = Integer.valueOf(curLine.trim().split(",")[0]);
            int node2 = Integer.valueOf(curLine.trim().split(",")[1]);
            ArrayList<Integer> neighbor1 = map.getOrDefault(node1, new ArrayList<>());
            neighbor1.add(node2);
            map.put(node1, neighbor1);
            ArrayList<Integer> neighbor2 = map.getOrDefault(node2, new ArrayList<>());
            neighbor2.add(node1);
            map.put(node2, neighbor2);
        }
    }

    public static boolean treeChecker() {
        if (!helper(0, -1, new ArrayList<>())) {
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

        for (int i : map.get(curr)) {
            path.add(curr);
            if (i != parent && !helper(i, curr, path)) {
                return false;
            }
            path.remove(path.size() - 1);

        }

        return true;
    }

    public static void main(String[] args) throws IOException{
        String path = "input_p1.txt";
        readFile(path);
        treeChecker();
    }
}
