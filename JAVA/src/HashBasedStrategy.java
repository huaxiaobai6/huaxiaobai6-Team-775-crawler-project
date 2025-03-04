import java.util.List;

public class HashBasedStrategy implements URLDistributionStrategy {
    private final List<String> queues = Arrays.asList("queue1", "queue2", "queue3");

    @Override
    public String getTargetQueue(String url) {
        int hash = url.hashCode();
        int idx = Math.abs(hash % queues.size());
        return queues.get(idx);
    }
}
