import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

public class RoundRobinStrategy implements URLDistributionStrategy {
    private final List<String> queues = Arrays.asList("queue1", "queue2", "queue3");
    private final AtomicInteger index = new AtomicInteger(0);

    @Override
    public String getTargetQueue(String url) {
        int idx = index.getAndIncrement() % queues.size();
        return queues.get(idx);
    }
}