import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;

public class FlinkURLDistributor {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // 1. 获取种子URL
        DataStream<String> inputStream = env.fromCollection(SeedURLManager.getSeedUrls());

        // 2. URL处理（去重、Robots协议检查）
        DataStream<String> processedStream = inputStream
                .filter(url -> RobotsChecker.isAllowed(url))
                .filter(url -> URLDeduplicator.isUnique(url));

        // 3. 分发策略（可配置）
        URLDistributionStrategy strategy = new RoundRobinStrategy(); // 或 HashBasedStrategy()

        // 4. 输出到消息队列
        processedStream.addSink(new RabbitMQSink(strategy));

        env.execute("Distributed URL Distributor");
    }
}
