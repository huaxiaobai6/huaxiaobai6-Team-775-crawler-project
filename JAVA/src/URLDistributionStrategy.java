public interface URLDistributionStrategy {
    String getTargetQueue(String url);
}