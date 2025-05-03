import java.util.*;
import java.util.concurrent.*;
import java.util.function.Function;

public class AdvancedCache<K, V> {
    private final ConcurrentHashMap<K, V> memoryCache = new ConcurrentHashMap<>();
    private final ConcurrentHashMap<K, Long> expiryTimes = new ConcurrentHashMap<>();
    private final ConcurrentHashMap<K, Long> accessTimes = new ConcurrentHashMap<>();
    private final PriorityQueue<K> lruQueue = new PriorityQueue<>(
        Comparator.comparingLong(k -> accessTimes.getOrDefault(k, 0L))
    );
    private final Function<K, V> loader;
    private final ScheduledExecutorService executor = Executors.newScheduledThreadPool(2);
    private final long maxSize;
    private final long defaultTtlMillis;

    public AdvancedCache(Function<K, V> loader, long maxSize, long defaultTtlMillis) {
        this.loader = loader;
        this.maxSize = maxSize;
        this.defaultTtlMillis = defaultTtlMillis;
        
        // Schedule regular cleanup
        executor.scheduleAtFixedRate(this::cleanup, 1, 1, TimeUnit.MINUTES);
    }

    public V get(K key) {
        return get(key, defaultTtlMillis);
    }

    public V get(K key, long ttlMillis) {
        // Check if expired
        if (isExpired(key)) {
            memoryCache.remove(key);
            expiryTimes.remove(key);
        }

        // Try memory cache
        V value = memoryCache.get(key);
        if (value != null) {
            accessTimes.put(key, System.currentTimeMillis());
            return value;
        }

        // Load data
        value = loader.apply(key);
        if (value != null) {
            put(key, value, ttlMillis);
        }
        return value;
    }

    public void put(K key, V value) {
        put(key, value, defaultTtlMillis);
    }

    public void put(K key, V value, long ttlMillis) {
        if (memoryCache.size() >= maxSize) {
            evict();
        }

        memoryCache.put(key, value);
        expiryTimes.put(key, System.currentTimeMillis() + ttlMillis);
        accessTimes.put(key, System.currentTimeMillis());
    }

    public void invalidate(K key) {
        memoryCache.remove(key);
        expiryTimes.remove(key);
        accessTimes.remove(key);
    }

    public void invalidateAll() {
        memoryCache.clear();
        expiryTimes.clear();
        accessTimes.clear();
    }

    private boolean isExpired(K key) {
        Long expiry = expiryTimes.get(key);
        return expiry != null && expiry < System.currentTimeMillis();
    }

    private void evict() {
        // LRU eviction policy
        K keyToEvict = lruQueue.poll();
        if (keyToEvict != null) {
            memoryCache.remove(keyToEvict);
            expiryTimes.remove(keyToEvict);
            accessTimes.remove(keyToEvict);
        }
    }

    private void cleanup() {
        long now = System.currentTimeMillis();
        List<K> toRemove = new ArrayList<>();

        for (Map.Entry<K, Long> entry : expiryTimes.entrySet()) {
            if (entry.getValue() < now) {
                toRemove.add(entry.getKey());
            }
        }

        for (K key : toRemove) {
            memoryCache.remove(key);
            expiryTimes.remove(key);
            accessTimes.remove(key);
        }

        // Rebuild LRU queue
        lruQueue.clear();
        lruQueue.addAll(accessTimes.keySet());
    }
}