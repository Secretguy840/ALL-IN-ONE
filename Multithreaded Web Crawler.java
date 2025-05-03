import java.util.*;
import java.util.concurrent.*;
import java.net.*;
import java.io.*;

public class WebCrawler {
    private final Set<String> visitedUrls = ConcurrentHashMap.newKeySet();
    private final Queue<String> urlQueue = new ConcurrentLinkedQueue<>();
    private final ExecutorService executor = Executors.newFixedThreadPool(10);

    public void crawl(String startUrl, int maxPages) {
        urlQueue.add(startUrl);
        
        List<Future<?>> futures = new ArrayList<>();
        for (int i = 0; i < maxPages; i++) {
            futures.add(executor.submit(this::crawlPage));
        }

        // Wait for completion
        futures.forEach(f -> {
            try { f.get(); } catch (Exception e) { e.printStackTrace(); }
        });
        executor.shutdown();
    }

    private void crawlPage() {
        String url;
        while ((url = urlQueue.poll()) != null) {
            if (!visitedUrls.add(url)) continue;
            
            try {
                System.out.println("Crawling: " + url);
                URLConnection connection = new URL(url).openConnection();
                BufferedReader reader = new BufferedReader(
                    new InputStreamReader(connection.getInputStream()));
                
                String line;
                while ((line = reader.readLine()) != null) {
                    // Simple URL extraction (real implementation would use regex)
                    if (line.contains("href=\"http")) {
                        int start = line.indexOf("href=\"") + 6;
                        int end = line.indexOf("\"", start);
                        String newUrl = line.substring(start, end);
                        urlQueue.add(newUrl);
                    }
                }
                reader.close();
            } catch (Exception e) {
                System.err.println("Error crawling " + url + ": " + e.getMessage());
            }
        }
    }

    public static void main(String[] args) {
        new WebCrawler().crawl("https://example.com", 50);
    }
}