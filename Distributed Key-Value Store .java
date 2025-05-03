import java.net.*;
import java.io.*;
import java.util.concurrent.*;
import java.util.*;

public class DistributedKVStore {
    private final Map<String, String> store = new ConcurrentHashMap<>();
    private final ServerSocket serverSocket;
    private final ExecutorService threadPool = Executors.newCachedThreadPool();

    public DistributedKVStore(int port) throws IOException {
        this.serverSocket = new ServerSocket(port);
        System.out.println("Server started on port " + port);
    }

    public void start() {
        while (true) {
            try {
                Socket clientSocket = serverSocket.accept();
                threadPool.execute(new ClientHandler(clientSocket));
            } catch (IOException e) {
                System.err.println("Server error: " + e.getMessage());
            }
        }
    }

    class ClientHandler implements Runnable {
        private final Socket socket;

        ClientHandler(Socket socket) {
            this.socket = socket;
        }

        @Override
        public void run() {
            try (BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                 PrintWriter out = new PrintWriter(socket.getOutputStream(), true)) {
                
                String inputLine;
                while ((inputLine = in.readLine()) != null) {
                    String[] parts = inputLine.split(" ");
                    String response;
                    
                    switch (parts[0]) {
                        case "GET":
                            response = store.getOrDefault(parts[1], "NOT_FOUND");
                            break;
                        case "PUT":
                            store.put(parts[1], parts[2]);
                            response = "OK";
                            break;
                        case "DELETE":
                            response = store.remove(parts[1]) != null ? "OK" : "NOT_FOUND";
                            break;
                        default:
                            response = "INVALID_COMMAND";
                    }
                    out.println(response);
                }
            } catch (IOException e) {
                System.err.println("Client handling error: " + e.getMessage());
            }
        }
    }

    public static void main(String[] args) throws IOException {
        new DistributedKVStore(8080).start();
    }
}