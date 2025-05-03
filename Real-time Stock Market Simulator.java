import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.stream.*;

public class StockMarketSimulator {
    static class Stock {
        final String symbol;
        final AtomicReference<Double> price;
        final AtomicInteger volume;
        final List<Double> priceHistory = new CopyOnWriteArrayList<>();

        Stock(String symbol, double initialPrice) {
            this.symbol = symbol;
            this.price = new AtomicReference<>(initialPrice);
            this.volume = new AtomicInteger(0);
            this.priceHistory.add(initialPrice);
        }

        void updatePrice() {
            double change = (ThreadLocalRandom.current().nextDouble() - 0.5) * 10;
            double newPrice = Math.max(1, price.get() + change);
            price.set(newPrice);
            priceHistory.add(newPrice);
            volume.incrementAndGet();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        List<Stock> stocks = Arrays.asList(
            new Stock("AAPL", 150.0),
            new Stock("GOOGL", 2800.0),
            new Stock("TSLA", 700.0),
            new Stock("AMZN", 3300.0)
        );

        ScheduledExecutorService executor = Executors.newScheduledThreadPool(4);
        stocks.forEach(stock -> 
            executor.scheduleAtFixedRate(stock::updatePrice, 0, 1, TimeUnit.SECONDS)
        );

        // Display updates
        executor.scheduleAtFixedRate(() -> {
            System.out.println("\n=== MARKET UPDATE ===");
            stocks.forEach(stock -> 
                System.out.printf("%s: $%.2f (Vol: %d)%n", 
                    stock.symbol, stock.price.get(), stock.volume.get())
            );
        }, 0, 5, TimeUnit.SECONDS);

        // Run for 1 minute
        Thread.sleep(60000);
        executor.shutdownNow();
    }
}